from django.shortcuts import render
import pymysql as mysql


def Actionsubcategoryinterface(request):
    try:
        rec = request.session['ADMIN_SES']
        return render(request, "subcategoryinterface.html", {'msg': ''})
    except:
        return render(request, "adminlogin.html", {'msg': ''})


def Actionsubcategorysubmit(request):
    scname = request.POST['scname']
    scdes = request.POST['scdes']
    cid = request.POST['cid']
    sfile = request.FILES['scicon']
    try:
        dbe = mysql.connect(host="localhost", port=3306,
                            user="root", password='', db="music")
        cmd = dbe.cursor()
        q = "INSERT INTO `subcategory` (`categoryid`, `scategoryname`, `scategorydescription`, `scategoryicon`) VALUES ('{}','{}','{}','{}')".format(
            cid, scname, scdes, sfile.name)
        cmd.execute(q)
        dbe.commit()
        dbe.close()
        # upload files
        f = open('C:/Users/Aman Gupta/musicvideo/asset/' + sfile.name, 'wb')
        for chunk in sfile.chunks():
            f.write(chunk)
        f.close()
        return render(request, "subcategoryinterface.html", {'msg': 'Record Submitted'})
    except Exception as e:
        print(e)
        return render(request, "subcategoryinterface.html", {'msg': 'Fail to Submit Record'})


def ActionsubcategoryDisplayAll(request):
    try:
        rec = request.session['ADMIN_SES']
        try:
            dbe = mysql.connect(host="localhost", port=3306,
                                user="root", password='', db="music")
            cmd = dbe.cursor()
            q = "select S.*, (select C.categoryname from category C where C.categoryid=S.categoryid) as categoryname  from subcategory S"
            cmd.execute(q)
            rows = cmd.fetchall()
            dbe.close()
            return render(request, "subcategorydisplayall.html", {'rows': rows})
        except Exception as e:
            print(e)
            return render(request, "subcategorydisplayall.html", {'rows': []})
    except:
        return render(request, "adminlogin.html", {'msg': ''})


def ActionsubcategoryDisplaybyid(request):
    try:
        scid = request.GET['scid']
        dbe = mysql.connect(host="localhost", port=3306,
                            user="root", password='', db="music")
        cmd = dbe.cursor()
        q = 'select S.*, (select C.categoryname from category C where C.categoryid=S.categoryid) as categoryname from subcategory S where S.scategoryid={}'.format(scid)
        cmd.execute(q)
        row = cmd.fetchone()
        dbe.close()
        return render(request, "subcategorydisplaybyid.html", {'row': row})
    except Exception as e:
        print(e)
        return render(request, "subcategorydisplaybyid.html", {'row': []})


def ActionsubCategoryEditDeleteSubmit(request):
    scid = request.POST['scid']
    cid = request.POST['cid']
    scname = request.POST['scname']
    scdes = request.POST['scdes']
    sbtn = request.POST['btn']
    try:
        if(sbtn == "Edit"):
            dbe = mysql.connect(host="localhost", port=3306,
                                user="root", password='', db="music")
            cmd = dbe.cursor()
            q = "update subcategory set categoryid='{}',scategoryname='{}',scategorydescription='{}' where scategoryid='{}'".format(
                cid, scname, scdes, scid)
            cmd.execute(q)
            dbe.commit()
            dbe.close()
            return ActionsubcategoryDisplayAll(request)
        elif(sbtn == "Delete"):
            dbe = mysql.connect(host="localhost", port=3306,
                                user="root", password='', db="music")
            cmd = dbe.cursor()
            q = "delete from subcategory where scategoryid='{}'".format(scid)
            cmd.execute(q)
            dbe.commit()
            dbe.close()
            return ActionsubcategoryDisplayAll(request)
    except Exception as e:
        print(e)
        return ActionsubcategoryDisplayAll(request)


def ActionEditsubCategoryPicture(request):
    scid = request.POST['scid']
    sfile = request.FILES['scicon']

    try:
        dbe = mysql.connect(host="localhost", port=3306,
                            user="root", password='', db="music")
        cmd = dbe.cursor()
        q = "update subcategory set scategoryicon='{}' where scategoryid={}".format(
            sfile.name, scid)
        cmd.execute(q)
        dbe.commit()
        dbe.close()
        f = open('C:/Users/Aman Gupta/musicvideo/asset/' + sfile.name, "wb")
        for chunk in sfile.chunks():
            f.write(chunk)
        f.close()
        return ActionsubcategoryDisplayAll(request)
    except Exception as e:
        print(e)
        return ActionsubcategoryDisplayAll(request)
