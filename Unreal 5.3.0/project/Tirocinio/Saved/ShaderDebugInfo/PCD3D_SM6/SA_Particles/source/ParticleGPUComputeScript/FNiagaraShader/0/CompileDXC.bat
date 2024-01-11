@ECHO OFF
SET DXC="E:\Unreal Engine\UE_5.3\Engine\Binaries\ThirdParty\ShaderConductor\Win64\dxc.exe"
IF NOT EXIST %DXC% (
	ECHO Couldn't find dxc.exe under "E:\Unreal Engine\UE_5.3\Engine\Binaries\ThirdParty\ShaderConductor\Win64"
	GOTO :END
)
%DXC% -Zpr -O3 -auto-binding-space 0 -Wno-parentheses-equality -disable-lifetime-markers -T cs_6_6 -E SimulateMainComputeCS -Fc NiagaraEmitterInstanceShader.d3dasm -Fo NiagaraEmitterInstanceShader.dxil NiagaraEmitterInstanceShader
:END
PAUSE
