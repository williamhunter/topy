#!/usr/bin/env python

from os import system, name

if name == 'posix':
    system('rm Q4.K')
    system('rm Q4bar.K')
    system('rm Q4T.K')
    system('rm Q5B.K')
    system('rm H8.K')
    system('rm H8T.K')
    system('rm H18B.K')
elif name == 'win32':
    system('del Q4.K')
    system('del Q4bar.K')
    system('del Q4T.K')
    system('del Q5B.K')
    system('del H8.K')
    system('del H8T.K')
    system('del H18B.K')
else:
    print 'This may take a while, perhaps a few minutes...'
    system('python Q4_K.py')
    print '1 of 7 done!'
    system('python Q4bar_K.py')
    print '2 of 7 done!'
    system('python Q4T_K.py')
    print '3 of 7 done!'
    system('python Q5B_K.py')
    print '4 of 7 done! All 2D matrices created. Now 3D...'
    system('python H8_K.py')
    print '5 of 7 done!'
    system('python H8T_K.py')
    print '6 of 7 done!'
    system('python H18B_K.py')
    print '7 of 7 done! All 3D matrices created. Finished.'

# EOF recreate_all.py
