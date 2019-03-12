
R=5.65;
L=46;
g=-9.8;

T=0.0529;

%Kp=6;
%Ki=3;
%Kd=12;


%%%RECUERDA CAMBIAR EL Ts EN EL PYTHON

contr=tf([Kd Kp Ki],[1 0]);
contrz=c2d(contr,T,'tustin')
Gs=tf([-g*5*R],[7*L 0 0]);
Ge=tf([-18.24],[0.0295 1]);
Gz=c2d(Gs,T,'zoh')
filter=filt([.3 .3],[1 .01])
%filter=filt([.5 .5],[1 .01])
sys=series(contrz,filter)
sys1=series(sys,Gz);
Glcz=feedback(sys1,1);
%step(Glcz);

[nume,deno]=tfdata(contrz,'v');
[num,den]=tfdata(sys,'v');

b0=num(1);
b1=num(2);
b2=num(3);
b3=num(4);
a0=den(1);
a1=den(2);
a2=den(3);
a3=den(4);


p1=-a1/a0;
p2=-a2/a0;
p3=-a3/a0;
p4=b0/a0;
p5=b1/a0;
p6=b2/a0;
p7=b3/a0;
v=[p1, p2, p3, p4, p5, p6, p7]

