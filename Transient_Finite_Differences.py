

def oneb(Fo, Bi, Tinf, nodes):
    Ti, Ta, Tb = nodes
    Tf = 2*Fo*(Ta + Tb + 2*Bi*Tinf) + (1-4*Fo - 4*Bi*Fo)*Ti
    return Tf


def twob(Fo, Bi, Tinf, nodes):
    Ti, Ta, Tb, Tc = nodes
    Tf = Fo*(2*Ta + Tb + Tc + 2*Bi*Tinf) + (1-4*Fo - 2*Bi*Fo)*Ti
    return Tf


def fourb(Fo, Bi, nodes):
    Ti, Ta, Tb, Tc, Td = nodes
    Tf = Fo*(Ta + Tb + Tc + Td) + (1-4*Fo)*Ti
    return Tf


def finite(Fo, Bi, Tinf, Ts, To):
    T1 = oneb(Fo, Bi, Tinf, (To[0], To[1], To[4]))
    T2 = twob(Fo, Bi, Tinf, (To[1], To[5], To[0], To[2]))
    T3 = twob(Fo, Bi, Tinf, (To[2], To[6], To[1], To[3]))
    T4 = twob(Fo, Bi, Tinf, (To[3], To[7], To[2], Ts))
    T5 = twob(Fo, Bi, Tinf, (To[4], To[5], To[0], To[8]))
    T9 = twob(Fo, Bi, Tinf, (To[8], To[9], To[4], To[12]))
    T13 = twob(Fo, Bi, Tinf, (To[12], To[13], To[8], Ts))
    T6 = fourb(Fo, Bi, (To[5], To[1], To[4], To[6], To[9]))
    T7 = fourb(Fo, Bi, (To[6], To[2], To[5], To[7], To[10]))
    T8 = fourb(Fo, Bi, (To[7], To[3], To[6], To[11], Ts))
    T10 = fourb(Fo, Bi, (To[9], To[5], To[8], To[10], To[13]))
    T11 = fourb(Fo, Bi, (To[10], To[6], To[9], To[11], To[14]))
    T12 = fourb(Fo, Bi, (To[11], To[7], To[10], To[15], Ts))
    T14 = fourb(Fo, Bi, (To[13], To[9], To[12], To[14], Ts))
    T15 = fourb(Fo, Bi, (To[14], To[10], To[13], To[15], Ts))
    T16 = fourb(Fo, Bi, (To[15], To[11], To[14], Ts, Ts))
    Tout = [T1, T2, T3, T4, T5, T6, T7, T8,
            T9, T10, T11, T12, T13, T14, T15, T16]
    return Tout


if __name__ == "__main__":
    h = 100
    k = 30
    rho = 1000
    cp = 3000
    dx = 0.05
    t = 300
    dt = 0.01
    Bi = h*dx/k
    Fo = k*dt/(rho*cp*dx**2)
    Tinf = 300
    Ts = 500
    To = [321.7, 324.2, 325.5, 324.2, 324.2, 327, 328.5, 327,
          325.5, 328.5, 330, 328.5, 324.2, 327, 328.5, 327]
    print(To)
    temp = finite(Fo, Bi, Tinf, Ts, To)
    for _ in range(int(t/dt)-1):
        # print(temp)
        temp = finite(Fo, Bi, Tinf, Ts, temp)
    for i in range(4):
        print(temp[i], temp[i+1], temp[i+2], temp[i+3])
    pass
