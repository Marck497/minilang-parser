price = 12.5;
units = 4;
total = price * units - 3;
IF total > (units + 30) :
    PRINT total;
    total = total - 10;
ELSE :
    PRINT 0;
ENDIF;
