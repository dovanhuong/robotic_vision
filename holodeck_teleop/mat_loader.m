clc
clear

load test.mat

t = 0:1/30:length(roll_c)/30;
t = t(1:end-1);

figure(1);clf
subplot(4,3,1)
plot (t,x)
title('x')

subplot(4,3,2)
plot (t,y)
title('y')

subplot(4,3,3)
plot (t,alt_c)
hold on
plot (t,z)
title('Altitude')
legend ('Commanded','Actual')

subplot(4,3,4)
plot (t,u)
title('u')

subplot(4,3,5)
plot (t,v)
title('v')

subplot(4,3,6)
plot (t,alt_c)
hold on
plot (t,w)
title('w')

subplot(4,3,7)
plot (t,-roll_c)
hold on 
plot (t,roll)
title('Roll')

subplot(4,3,8)
plot (t,pitch_c)
hold on 
plot (t,pitch)
title('Pitch')

subplot(4,3,9)
hold on 
plot (t,yaw)
title('Yaw')

subplot(4,3,10)
hold on 
plot (t,p)
title('p')

subplot(4,3,11)
hold on 
plot (t,q)
title('q')

subplot(4,3,12)
hold on 
plot (t,yaw_c)
plot (t,r)
title('r')

