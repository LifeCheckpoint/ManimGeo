from manimlib import *
from manimgeo.components import *
from manimgeo.anime.manimgl import GeoManimGLManager

# Developed

"""
注意：
正 257 边形的绘制较为复杂，其关键步骤为计算 Cos[2Pi/257]
这里将使用来自 https://zhuanlan.zhihu.com/p/384287969 的计算方法
逐步分解得出计算过程

计算方式 (Mathematica)
A0=Root[x^2+x-64,2]
A1=Root[x^2+x-64,1]
B0=Simplify[Root[x^2-A0*x-16,2]]
B1=Simplify[Root[x^2-A1*x-16,2]]
B2=Simplify[Root[x^2-A0*x-16,1]]
B3=Simplify[Root[x^2-A1*x-16,1]]
C0=Simplify[Root[x^2-B0*x-A0-2*B0-5,2]]
C1=Simplify[Root[x^2-B1*x-A1-2*B1-5,1]]
C2=Simplify[Root[x^2-B2*x-A0-2*B2-5,2]]
C3=Simplify[Root[x^2-B3*x-A1-2*B3-5,1]]
C4=Simplify[Root[x^2-B0*x-A0-2*B0-5,1]]
C5=Simplify[Root[x^2-B1*x-A1-2*B1-5,2]]
C6=Simplify[Root[x^2-B2*x-A0-2*B2-5,1]]
C7=Simplify[Root[x^2-B3*x-A1-2*B3-5,2]]
D0=Simplify[Root[x^2-C0*x+A0+C0+C2+2 C5,2]]
D1=Simplify[Root[x^2-C1*x+A1+C1+C3+2 C6,2]]
D2=Simplify[Root[x^2-C2*x+A0+C2+C4+2 C7,2]]
D3=Simplify[Root[x^2-C3*x+A1+C3+C5+2 C0,2]]
D4=Simplify[Root[x^2-C4*x+A0+C4+C6+2 C1,2]]
D5=Simplify[Root[x^2-C5*x+A1+C5+C7+2 C2,2]]
D6=Simplify[Root[x^2-C6*x+A0+C6+C0+2 C3,1]]
D7=Simplify[Root[x^2-C7*x+A1+C7+C1+2 C4,2]]
D8=Simplify[Root[x^2-C0*x+A0+C0+C2+2 C5,1]]
D9=Simplify[Root[x^2-C1*x+A1+C1+C3+2 C6,1]]
D10=Simplify[Root[x^2-C2*x+A0+C2+C4+2 C7,1]]
D11=Simplify[Root[x^2-C3*x+A1+C3+C5+2 C0,1]]
D12=Simplify[Root[x^2-C4*x+A0+C4+C6+2 C1,1]]
D13=Simplify[Root[x^2-C5*x+A1+C5+C7+2 C2,1]]
D14=Simplify[Root[x^2-C6*x+A0+C6+C0+2 C3,2]]
D15=Simplify[Root[x^2-C7*x+A1+C7+C1+2 C4,1]]
E0=Root[x^2-D0*x+D0+D1+D2+D5,2]
E1=Root[x^2-D1*x+D1+D2+D3+D6,2]
E7=Root[x^2-D7*x+D7+D8+D9+D12,1]
E8=Root[x^2-D8*x+D8+D9+D10+D13,1]
E9=Root[x^2-D9*x+D9+D10+D11+D14,1]
E15=Root[x^2-D15*x+D15+D0+D1+D4,2]
E16=Root[x^2-D0*x+D0+D1+D2+D5,1]
E17=Root[x^2-D1*x+D1+D2+D3+D6,1]
E23=Root[x^2-D7*x+D7+D8+D9+D12,2]
E24=Root[x^2-D8*x+D8+D9+D10+D13,2]
E25=Root[x^2-D9*x+D9+D10+D11+D14,2]
E31=Root[x^2-D15*x+D15+D0+D1+D4,1]
F0=Root[x^2-E0*x+E1+E23,2]
F24=Root[x^2-E24*x+E15+E25,1]
F32=Root[x^2-E0*x+E1+E23,1]
F56=Root[x^2-E24*x+E15+E25,2]
G0=Root[x^2-F0*x+F56,2]
X=Sqrt[(1-G0/2)/2]
"""

