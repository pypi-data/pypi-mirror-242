import os
import json
from time import sleep
from multiprocessing import Pool
import subprocess
import threading

from win32com.client import Dispatch, DispatchEx
import win32process
import win32api
import win32con
from pywinauto import Application
from pywinauto.application import ProcessNotFoundError

from femtetutils import util, const

print_progress = True
if print_progress:
    import optuna
    optuna.logging.disable_default_handler()

from PyFemtet.opt.core import FEMSystem

import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=r"32-bit")
warnings.filterwarnings("ignore", category=UserWarning, message=r"64-bit")


here, me = os.path.split(__file__)


# ユーザーは設定しない定数
PATH_JOURNAL = os.path.abspath(os.path.join(here, 'update_model_parameter.py'))


def _f(objective_functions, objective_arguments, constraint_functions, constraint_arguments):
    # if print_progress:
    #     print('NX_Femtet solve Femtet / start')

    # インスタンスメソッドにしたら動かない
    # クラスメソッドにしても動かない。なんでだろう？
    # 新しいプロセスで呼ぶ関数。
    # 新しい Femtet を作って objectives を計算する
    # その後、プロセスは死ぬので Femtet は解放される
    # TODO:この関数の最後で、Femtet を殺していいかどうか検討する
    Femtet = Dispatch('FemtetMacro.Femtet')
    from .core import MeshError, SolveError
    try:
        Femtet.Gaudi.Mesh()
    except:
        raise MeshError
    try:
        Femtet.Solve()
    except:
        raise SolveError

    # if print_progress:
    #     print('NX_Femtet solve Femtet / end')
    #     print('NX_Femtet calc objectives / start')

    Femtet.OpenCurrentResult(True)
    ret_objective = []
    ret_constraint = []
    for func, (args, kwargs) in zip(objective_functions, objective_arguments):
        ret_objective.append(func(Femtet, *args, **kwargs))
    for func, (args, kwargs) in zip(constraint_functions, constraint_arguments):
        ret_constraint.append(func(Femtet, *args, **kwargs))

    # if print_progress:
    #     print('NX_Femtet calc objectives / end')

    return ret_objective, ret_constraint



class NX_Femtet(FEMSystem):
    def __init__(self, path_prt):
        self._path_prt = os.path.abspath(path_prt)
        self._path_bas = None
        self._path_xlsm = None
        self._stop_excel_watcher = False
        self.excel = None
        
        femtet_dir = os.path.split(util.get_femtet_exe_path())[0]
        self._path_macro = os.path.join(femtet_dir, 'Macro32/FemtetMacro.dll')
        self._path_ref = os.path.join(femtet_dir, 'Macro32/FemtetRef.xla')

    def set_bas(self, path_bas):
        self._path_bas = os.path.abspath(path_bas)
        self._path_xlsm = None

    def set_excel(self, path_xlsx):
        self._path_xlsm = os.path.abspath(path_xlsx)
        self._path_bas = None
            
    def run(self):
        # 使わないけど FEMSystem が実装を求めるためダミーで作成
        pass
    
    def f(self, df, objectives, constraints):
        if print_progress:
            print('')
            print('NX_Femtet iteration / start')

        from PyFemtet.opt.core import ModelError, MeshError, SolveError

        if print_progress:
            print('  start update model via NX')

        try:
            self._update_model(df)
        except ModelError as e:
            print('failed to create model via NX')
            raise e

        if print_progress:
            print('  end update model via NX')
            print('  start Femtet setup via Excel')

        try:
            self._setup_new_Femtet()
        except ModelError as e:
            print('failed to setup model via Excel-Femtet')
            raise e

        if print_progress:
            print('  end Femtet setup via Excel')
            print('  start solve')

        try:
            self._run_new_Femtet(objectives, constraints)
        except (MeshError, SolveError) as e:
            print('failed to mesh or solve via FEMOpt-Femtet')
            raise e

        if print_progress:
            print('  end Excel-Femtet')
            print('NX_Femtet iteration / end')

        return self.objectiveValues, self.constraintValues
            
    def _update_model(self, df):
        # run_journal を使って prt から x_t を作る
        # prt と同じ名前の x_t ができる
        # 先にそれを消しておく
        path_x_t = os.path.splitext(self._path_prt)[0] + '.x_t'
        if os.path.isfile(path_x_t):
            os.remove(path_x_t)
        exe = r'%UGII_BASE_DIR%\NXBIN\run_journal.exe'
        tmp = dict(zip(df.name.values, df.value.values.astype(str)))
        strDict = json.dumps(tmp)
        env = os.environ.copy()
        subprocess.run(
            [exe, PATH_JOURNAL, '-args', self._path_prt, strDict],
            env=env,
            shell=True,
            cwd=os.path.dirname(self._path_prt))
        # この時点で x_t ファイルがなければモデルエラー
        if not os.path.isfile(path_x_t):
            from PyFemtet.opt.core import ModelError
            raise ModelError

    def _set_reference_of_new_excel(self, wb):
        try:
            wb.VBProject.References.AddFromFile(self._path_macro)
        except:
            pass
        try:
            wb.VBProject.References.AddFromFile(self._path_ref)
        except:
            pass
        
    
    def _setup_new_Femtet(self):
        # excel 経由で bas を使って x_t から Femtet のセットアップをする
        # その後、excel は殺す
        # excel の立ち上げ
        self.excel = DispatchEx("Excel.Application")
        self.excel.Visible = False
        self.excel.DisplayAlerts = False
        
        # bas 指定の場合：新しい xlsm を作る
        if self._path_bas is not None:
            # wb の準備
            wb = self.excel.Workbooks.Add()
            # マクロのセットアップ
            wb.VBProject.VBComponents.Import(self._path_bas)
            self._set_reference_of_new_excel(wb)

        # xlsm 指定の場合：開く
        elif self._path_xlsm is not None:
            # wb の準備
            wb = self.excel.Workbooks.Open(self._path_xlsm)
            # マクロのセットアップ
            self._set_reference_of_new_excel(wb)

        # Saved にしておけば自動回復ファイルが保存されない
        while True:
            try:
                wb.Saved = True
                break
            except AttributeError: # wb が開く前に Saved が走る対策
                continue
        
        # excel VBA エラー監視スレッドの開始
        self._stop_excel_watcher = False
        _, pid = win32process.GetWindowThreadProcessId(self.excel.Hwnd)
        t = threading.Thread(target=_excel_watcher, args=(pid, self))
        t.start()

        # Femtet セットアップの実行
        from .core import ModelError
        from pythoncom import com_error
        try:
            self.excel.Run('FemtetMacro.FemtetMain')
        except com_error:
            # エラーが発生している場合は excel_watcher が
            # excel のプロセスを終了しているから何もしなくていい
            raise ModelError
        else:
            # 問題なく終了すれば、スレッドを閉じるフラグを立てる
            self._stop_excel_watcher = True
            sleep(1) # スレッドの終了を一応待つ
            # 保存せずに閉じる
            wb.Close()
            # 終了
            self._close_excel_by_force()

    def _run_new_Femtet(self, objectives, constraints):
        # Python のサブプロセスで目的関数の計算を適用する
        # （メインプロセスでやるとサブスレッドであっても Femtet を捕まえて次の Excel 処理に渡さなくなる）
        obj_functions = [obj.ptrFunc for obj in objectives]
        obj_arguments = [(obj.args, obj.kwargs) for obj in objectives]
        cons_functions = [obj.ptrFunc for obj in constraints]
        cons_arguments = [(obj.args, obj.kwargs) for obj in constraints]

        if print_progress:
            print('    start Pool')
        
        with Pool(processes=1) as p:
            obj_result, cons_result = p.apply(_f, (obj_functions, obj_arguments, cons_functions, cons_arguments))
            self.objectiveValues = obj_result
            self.constraintValues = cons_result

        if print_progress:
            print('    end Pool')
        
    def _close_excel_by_force(self):
        # プロセス ID の取得
        hwnd = self.excel.Hwnd
        _, p = win32process.GetWindowThreadProcessId(hwnd)
        # force close
        try:
            handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, p)
            if handle:
                win32api.TerminateProcess(handle, 0)
                win32api.CloseHandle(handle)
        except:
            pass



def _get_excel_state(pid, timeout=1):
    '''
    excel がなければ 0, あれば 1
    あって、さらに「Microsoft Visual Basic」ダイアログがあれば -1 を返す
    '''
    
    # Excelのアプリケーションを取得
    try:
        app = Application().connect(process=pid)
    except ProcessNotFoundError:
        return 0
    
    # ダイアログの存在の有無
    try:
        app.window(title="Microsoft Visual Basic").wait('exists', timeout=timeout)
        return -1
    except:
        sleep(timeout)
        return 1


def _excel_watcher(pid, stopper:NX_Femtet):
    if print_progress:
        print('    excel_watcher has been launched')
    # threading に呼ばれ、1秒ごとに excel の状態を監視
    # エラーが出ていれば excel を終了して仕事を終了する
    # excel が終了していれば仕事を終了する
    while True:
        excel_state = _get_excel_state(pid, timeout=1)
        if print_progress:
            print('    excel state is ', excel_state)
        if excel_state==-1:
            # excel を強制終了して break する
            try:
                handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pid)
                if handle:
                    win32api.TerminateProcess(handle, 0)
                    win32api.CloseHandle(handle)
            except:
                pass
            break
        if excel_state==0:
            # 終了する
            break
        if stopper._stop_excel_watcher:
            # 終了する
            break
    if print_progress:
        print('    excel_watcher will be terminated successfully')
    return None # thread 終了

#     print(FEMOpt.f(df, [get_flow]))
    