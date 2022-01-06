update C set cname='李四' where cno='C001';
update C set addr='南京' where cno='C001';
update S set price=price*0.95 where sname='可乐';
update S set inventory=inventory+10 where sname='可乐';
update S set inventory=inventory-10 where sname='可乐';
update C,S,GS,G set gnum=gnum-10 where C.cno=G.cno and GS.gno=G.gno and GS.sno=S.sno and sname='可乐';
update C,S,GS,G set gnum=gnum+10 where C.cno=G.cno and GS.gno=G.gno and GS.sno=S.sno and sname='可乐';
update C,D set pay_yn='Y' where C.cno=D.cno and C.cno='C001';
update C,D set s_yn='Y' where C.cno=D.cno and C.cno='C001';