Attribute VB_Name = "FemtetMacro"
Option Explicit

Dim FEMTET As New CFemtet
Dim Als As CAnalysis
Dim BodyAttr As CBodyAttribute
Dim Bnd As CBoundary
Dim Mtl As CMaterial
Dim Gaudi As CGaudi
Dim Gogh As CGogh
'/////////////////////////null***�̐���/////////////////////////
'//���L�̎l�̕ϐ���CGaudi�N���XMulti***���g�p����ꍇ�ɗp���܂��B
'//�Ⴆ��MultiFillet���g�p����ꍇ�Ɉ����ł���Vertex(�_)�͎w�肹��
'//������Edge(��)������Fillet����ꍇ��nullVertex()��p���܂��B
'//�uGaudi.MultiFillet nullVertex,Edge�v�Ƃ����
'//������Edge����Fillet���邱�Ƃ��ł��܂��B
'/////////////////////////////////////////////////////////////
Global nullVertex() As CGaudiVertex
Global nullEdge() As CGaudiEdge
Global nullFace() As CGaudiFace
Global nullBody() As CGaudiBody

'///////////////////////////////////////////////////

'�ϐ��̐錾
Private pi As Double
'///////////////////////////////////////////////////


'////////////////////////////////////////////////////////////
'    Main�֐�
'////////////////////////////////////////////////////////////
Sub FemtetMain()
    '------- Femtet�����N�� (�s�v�ȏꍇ��Excel�Ŏ��s���Ȃ��ꍇ�͉��s���R�����g�A�E�g���Ă�������) -------
    Workbooks("FemtetRef.xla").AutoExecuteFemtet

    '------- �V�K�v���W�F�N�g -------
    If FEMTET.OpenNewProject() = False Then
        FEMTET.ShowLastError
    End If

    '------- �ϐ��̒�` -------
    InitVariables

    '------- �f�[�^�x�[�X�̐ݒ� -------
    AnalysisSetUp
    BodyAttributeSetUp
    MaterialSetUp
    BoundarySetUp

    '------- ���f���̍쐬 -------
    Set Gaudi = FEMTET.Gaudi
    MakeModel

    '------- �W�����b�V���T�C�Y�̐ݒ� -------
    '<<<<<<< �����v�Z�ɐݒ肷��ꍇ��-1��ݒ肵�Ă������� >>>>>>>
    Gaudi.MeshSize = 4


    '------- ���b�V���̐��� -------
    '<<<<<<< ���b�V���𐶐�����ꍇ�͈ȉ��̃R�����g���O���Ă������� >>>>>>>
    'Gaudi.Mesh

    '------- ��͂̎��s -------
    '<<<<<<< ��͂����s����ꍇ�͈ȉ��̃R�����g���O���Ă������� >>>>>>>
    'Femtet.Solve

    '------- ��͌��ʂ̒��o -------
    '<<<<<<< �v�Z���ʂ𒊏o����ꍇ�͈ȉ��̃R�����g���O���Ă������� >>>>>>>
    'SamplingResult

    '------- �v�Z���ʂ̕ۑ� -------
    '<<<<<<< �v�Z����(.pdt)�t�@�C����ۑ�����ꍇ�͈ȉ��̃R�����g���O���Ă������� >>>>>>>
    'If Femtet.SavePDT(Femtet.ResultFilePath & ".pdt", True) = False Then
    '    Femtet.ShowLastError
    'End If

End Sub

'////////////////////////////////////////////////////////////
'    ��͏����̐ݒ�
'////////////////////////////////////////////////////////////
Sub AnalysisSetUp()

    '------- �ϐ��ɃI�u�W�F�N�g�̐ݒ� -------
    Set Als = FEMTET.Analysis

    '------- ��͏�������(Common) -------
    Als.AnalysisType = GALILEO_C

    '------- ����(Gauss) -------
    Als.Gauss.b2ndEdgeElement = True

    '------- ����(Galileo) -------
    Als.Galileo.bResultDetail = True

    '------- �d���g(Hertz) -------
    Als.Hertz.b2ndEdgeElement = True

    '------- ���a���(Harmonic) -------
    Als.Harmonic.FreqSweepType = LINEAR_INTERVAL_C

    '------- �ߓn���(Transient) -------
    Als.Transient.bAuto = False

    '------- �M�׏d(ThermalStress) -------
    Als.ThermalStress.Temp = (25#)
    Als.ThermalStress.TempRef = (25#)

    '------- ���x�Ȑݒ�(HighLevel) -------
    Als.HighLevel.MemoryLimit = (32)

    '------- ���b�V���̐ݒ�(MeshProperty) -------
    Als.MeshProperty.bAdaptiveMeshOnCurve = True
    Als.MeshProperty.bAutoCalcAutoAirMeshSize = False
    Als.MeshProperty.AutoAirMeshSize = (60#)
    Als.MeshProperty.bChangePlane = True
    Als.MeshProperty.bMeshG2 = True
    Als.MeshProperty.bPeriodMesh = False

    '------- �����X�e�b�v�ݒ�(StepAnalysis) -------
    Als.StepAnalysis.Set_Table_withoutTime 0, (20), (25#)

    '------- ���ʃC���|�[�g(Import) -------
    Als.Import.AnalysisModelName = "���I��"
End Sub

'////////////////////////////////////////////////////////////
'    Body�����S�̂̐ݒ�
'////////////////////////////////////////////////////////////
Sub BodyAttributeSetUp()

    '------- �ϐ��ɃI�u�W�F�N�g�̐ݒ� -------
    Set BodyAttr = FEMTET.BodyAttribute

    '------- Body�����̐ݒ� -------
    BodyAttributeSetUp_�{�f�B����_001
End Sub

'////////////////////////////////////////////////////////////
'    Body�����̐ݒ� Body�������F�{�f�B����_001
'////////////////////////////////////////////////////////////
Sub BodyAttributeSetUp_�{�f�B����_001()
    '------- Body������Index��ۑ�����ϐ� -------
    Dim Index As Integer

    '------- Body�����̒ǉ� -------
    BodyAttr.Add "�{�f�B����_001"

    '------- Body���� Index�̐ݒ� -------
    Index = BodyAttr.Ask("�{�f�B����_001")

    '------- �V�[�g�{�f�B�̌��� or 2������͂̉��s��(BodyThickness)/���C���[�{�f�B��(WireWidth) -------
    BodyAttr.Length(Index).bUseAnalysisThickness2D = True

    '------- ����(Direction) -------
    BodyAttr.Direction(Index).SetAxisVector (0#), (0#), (1#)

    '------- �������x(InitialVelocity) -------
    BodyAttr.InitialVelocity(Index).bAnalysisUse = True

    '------- ����(FluidBern) -------
    BodyAttr.FluidAttribute(Index).FlowCondition.bSpline = False

    '------- �t��(Emittivity) -------
    BodyAttr.ThermalSurface(Index).Emittivity.Eps = (0.8)
End Sub

'////////////////////////////////////////////////////////////
'    Material�S�̂̐ݒ�
'////////////////////////////////////////////////////////////
Sub MaterialSetUp()

    '------- �ϐ��ɃI�u�W�F�N�g�̐ݒ� -------
    Set Mtl = FEMTET.Material

    '------- Material�̐ݒ� -------
    MaterialSetUp_007_�SFe
End Sub

'////////////////////////////////////////////////////////////
'    Material�̐ݒ� Material���F007_�SFe
'////////////////////////////////////////////////////////////
Sub MaterialSetUp_007_�SFe()
    '------- Material��Index��ۑ�����ϐ� -------
    Dim Index As Integer

    '------- Material�̒ǉ� -------
    Mtl.Add "007_�SFe"

    '------- Material Index�̐ݒ� -------
    Index = Mtl.Ask("007_�SFe")

    '------- ������(Permeability) -------
    Mtl.Permeability(Index).sMu = (5000)

    '------- ��R��(Resistivity) -------
    Mtl.Resistivity(Index).sRho = (9.71) * 10 ^ (-8)
    Mtl.Resistivity(Index).bSpline = False
    Mtl.Resistivity(Index).Set_Table 0, (-195), (0.07) * 10 ^ (-7)
    Mtl.Resistivity(Index).Set_Table 1, (0), (0.89) * 10 ^ (-7)
    Mtl.Resistivity(Index).Set_Table 2, (100), (1.47) * 10 ^ (-7)
    Mtl.Resistivity(Index).Set_Table 3, (300), (3.15) * 10 ^ (-7)
    Mtl.Resistivity(Index).Set_Table 4, (700), (8.55) * 10 ^ (-7)

    '------- ���d��(ElectricConductivity) -------
    Mtl.ElectricConductivity(Index).ConductorType = CONDUCTOR_C
    Mtl.ElectricConductivity(Index).sSigma = (1.03) * 10 ^ (7)

    '------- ��M(SpecificHeat) -------
    Mtl.SpecificHeat(Index).C = (451.786193929627)
    Mtl.SpecificHeat(Index).bSpline = False
    Mtl.SpecificHeat(Index).Set_Table 0, (-173), (0.2157758080401) * 10 ^ (3)
    Mtl.SpecificHeat(Index).Set_Table 1, (-73), (0.3842779120781) * 10 ^ (3)
    Mtl.SpecificHeat(Index).Set_Table 2, (20), (0.4517861939296) * 10 ^ (3)
    Mtl.SpecificHeat(Index).Set_Table 3, (127), (0.4906437460829) * 10 ^ (3)
    Mtl.SpecificHeat(Index).Set_Table 4, (327), (0.5658519115409) * 10 ^ (3)

    '------- ���x(Density) -------
    Mtl.Density(Index).Dens = (7874)

    '------- �M�`����(ThermalConductivity) -------
    Mtl.ThermalConductivity(Index).sRmd = (80.3)
    Mtl.ThermalConductivity(Index).bSpline = False
    Mtl.ThermalConductivity(Index).Set_Table 0, (-173), (132)
    Mtl.ThermalConductivity(Index).Set_Table 1, (-73), (94)
    Mtl.ThermalConductivity(Index).Set_Table 2, (27), (80.3)
    Mtl.ThermalConductivity(Index).Set_Table 3, (127), (69.4)

    '------- ���c���W��(Expansion) -------
    Mtl.Expansion(Index).sAlf = (1.18) * 10 ^ (-5)
    Mtl.Expansion(Index).bSpline = False
    Mtl.Expansion(Index).Set_Table 0, (-173), (0.56) * 10 ^ (-5)
    Mtl.Expansion(Index).Set_Table 1, (20), (1.18) * 10 ^ (-5)
    Mtl.Expansion(Index).Set_Table 2, (227), (1.44) * 10 ^ (-5)
    Mtl.Expansion(Index).Set_Table 3, (527), (1.62) * 10 ^ (-5)

    '------- �e���萔(Elasticity) -------
    Mtl.Elasticity(Index).sY = (206) * 10 ^ (9)
    Mtl.Elasticity(Index).Nu = (0.28)

    '------- ���d�萔(PiezoElectricity) -------
    Mtl.PiezoElectricity(Index).bPiezo = False

    '------- ���� -------
    Mtl.Comment(Index).Comment = "�s�o�T�t " & Chr(13) & Chr(10) & "�@���x�F [C2]P.26" & Chr(13) & Chr(10) & "�@�e���萔�F [C2]P.26" & Chr(13) & Chr(10) & "�@���c���W���F [S]P.484" & Chr(13) & Chr(10) & "�@��R���F [C2]P.490, [S]P.527" & Chr(13) & Chr(10) & "�@��M�F [S]P.473" & Chr(13) & Chr(10) & "�@�M�`�����F [C2]P.70" & Chr(13) & Chr(10) & "�@�@" & Chr(13) & Chr(10) & "�s�Q�l�����t�@" & Chr(13) & Chr(10) & "�@[C2] ���w�֗� ��b��II ����4�� ���{���w�w��� �ۑP(1993)" & Chr(13) & Chr(10) & "�@[S] ���ȔN�\ ����8�N �����V����� �ۑP(1996)"
End Sub

'////////////////////////////////////////////////////////////
'    Boundary�S�̂̐ݒ�
'////////////////////////////////////////////////////////////
Sub BoundarySetUp()

    '------- �ϐ��ɃI�u�W�F�N�g�̐ݒ� -------
    Set Bnd = FEMTET.Boundary

    '------- Boundary�̐ݒ� -------
    BoundarySetUp_RESERVED_default
    BoundarySetUp_fix
    BoundarySetUp_load
End Sub

'////////////////////////////////////////////////////////////
'    Boundary�̐ݒ� Boundary���FRESERVED_default (�O�����E����)
'////////////////////////////////////////////////////////////
Sub BoundarySetUp_RESERVED_default()
    '------- Boundary��Index��ۑ�����ϐ� -------
    Dim Index As Integer

    '------- Boundary�̒ǉ� -------
    Bnd.Add "RESERVED_default"

    '------- Boundary Index�̐ݒ� -------
    Index = Bnd.Ask("RESERVED_default")

    '------- �M(Thermal) -------
    Bnd.Thermal(Index).bConAuto = True
    Bnd.Thermal(Index).bSetRadioSetting = False

    '------- ����_�����x(RoomTemp) -------
    Bnd.Thermal(Index).RoomTemp.TempType = TEMP_AMBIENT_C

    '------- �t��(Emittivity) -------
    Bnd.Thermal(Index).Emittivity.Eps = (0.8)
End Sub

'////////////////////////////////////////////////////////////
'    Boundary�̐ݒ� Boundary���Ffix
'////////////////////////////////////////////////////////////
Sub BoundarySetUp_fix()
    '------- Boundary��Index��ۑ�����ϐ� -------
    Dim Index As Integer

    '------- Boundary�̒ǉ� -------
    Bnd.Add "fix"

    '------- Boundary Index�̐ݒ� -------
    Index = Bnd.Ask("fix")

    '------- �@�B(Mechanical) -------
    Bnd.Mechanical(Index).Condition = DISPLACEMENT_C

    '------- �M(Thermal) -------
    Bnd.Thermal(Index).bConAuto = True
    Bnd.Thermal(Index).bSetRadioSetting = False

    '------- ����_�����x(RoomTemp) -------
    Bnd.Thermal(Index).RoomTemp.TempType = TEMP_AMBIENT_C

    '------- �t��(Emittivity) -------
    Bnd.Thermal(Index).Emittivity.Eps = (0.8)

    '------- ����(FluidBern) -------
    Bnd.FluidBern(Index).bSpline = True
End Sub

'////////////////////////////////////////////////////////////
'    Boundary�̐ݒ� Boundary���Fload
'////////////////////////////////////////////////////////////
Sub BoundarySetUp_load()
    '------- Boundary��Index��ۑ�����ϐ� -------
    Dim Index As Integer

    '------- Boundary�̒ǉ� -------
    Bnd.Add "load"

    '------- Boundary Index�̐ݒ� -------
    Index = Bnd.Ask("load")

    '------- �@�B(Mechanical) -------
    Bnd.Mechanical(Index).Condition = FACE_LOAD_C
    Bnd.Mechanical(Index).SetT (0#), (0#), (-10)
    Bnd.Mechanical(Index).SetTM (0), (0), (0)
    Bnd.Mechanical(Index).bT = True

    '------- �M(Thermal) -------
    Bnd.Thermal(Index).bConAuto = True
    Bnd.Thermal(Index).bSetRadioSetting = False

    '------- ����_�����x(RoomTemp) -------
    Bnd.Thermal(Index).RoomTemp.TempType = TEMP_AMBIENT_C

    '------- �t��(Emittivity) -------
    Bnd.Thermal(Index).Emittivity.Eps = (0.8)

    '------- ����(FluidBern) -------
    Bnd.FluidBern(Index).bSpline = True
End Sub

'////////////////////////////////////////////////////////////
'    IF�֐�
'////////////////////////////////////////////////////////////
Function F_IF(expression As Double, val_true As Double, val_false As Double) As Double
    If expression Then
        F_IF = val_true
    Else
        F_IF = val_false
    End If

End Function

'////////////////////////////////////////////////////////////
'    �ϐ���`�֐�
'////////////////////////////////////////////////////////////
Sub InitVariables()


    'VB��̕ϐ��̒�`
    pi = 3.14159265358979

    'FemtetGUI��̕ϐ��̓o�^�i�������f���̕ϐ����䓙�ł̂ݗ��p�j

End Sub

'////////////////////////////////////////////////////////////
'    ���f���쐬�֐�
'////////////////////////////////////////////////////////////
Sub MakeModel()

    '------- Body�z��ϐ��̒�` -------
    Dim Body() As CGaudiBody

    '------- ���f����`�悳���Ȃ��ݒ� -------
    FEMTET.RedrawMode = False


    '------- Import2 -------
    ReDim Preserve Body(0)
    Dim BodyArray0() As CGaudiBody
    Gaudi.Import2 ThisWorkbook.Path + "\NXTEST.x_t", True, BodyArray0, False
    Set Body(0) = BodyArray0(0)

    '------- SetName -------
    Body(0).SetName "�{�f�B����_001", "007_�SFe"

    '------- SetBoundary -------
    Dim Face0(1) As CGaudiFace
    Set Face0(0) = Body(0).GetFaceByID(315)
    Set Face0(1) = Body(0).GetFaceByID(329)
    Gaudi.MultiSetBoundary nullVertex, nullEdge, Face0, nullBody, "fix"

    '------- SetBoundary -------
    Dim Face1 As CGaudiFace
    Set Face1 = Body(0).GetFaceByID(317)
    Face1.SetBoundary "load"


    '------- ���f�����ĕ`�悵�܂� -------
    FEMTET.Redraw

End Sub

'////////////////////////////////////////////////////////////
'    �v�Z���ʒ��o�֐�
'////////////////////////////////////////////////////////////
Sub SamplingResult()

    '------- �ϐ��ɃI�u�W�F�N�g�̐ݒ� -------
    Set Gogh = FEMTET.Gogh

    '------- ���݂̌v�Z���ʂ𒆊ԃt�@�C������J�� -------
    If FEMTET.OpenCurrentResult(True) = False Then
        FEMTET.ShowLastError
    End If

    '------- �t�B�[���h�̐ݒ� -------
    Gogh.Galileo.Vector = GALILEO_DISPLACEMENT_C

    '------- �ő�l�̎擾 -------
    Dim PosMax() As Double '�ő�l�̍��W
    Dim ResultMax As Double ' �ő�l

    If Gogh.Galileo.GetMAXVectorPoint(VEC_C, CMPX_REAL_C, PosMax, ResultMax) = False Then
        FEMTET.ShowLastError
    End If

    '------- �ŏ��l�̎擾 -------
    Dim PosMin() As Double '�ŏ��l�̍��W
    Dim ResultMin As Double '�ŏ��l

    If Gogh.Galileo.GetMINVectorPoint(VEC_C, CMPX_REAL_C, PosMin, ResultMin) = False Then
        FEMTET.ShowLastError
    End If

    '------- �C�Ӎ��W�̌v�Z���ʂ̎擾 -------
    Dim Value() As New CComplex

    If Gogh.Galileo.GetVectorAtPoint(100, 5, 50, Value()) = False Then
        FEMTET.ShowLastError
    End If

    ' �����̍��W�̌��ʂ��܂Ƃ߂Ď擾����ꍇ�́AMultiGetVectorAtPoint�֐��������p���������B

End Sub

