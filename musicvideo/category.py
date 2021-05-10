from django.shortcuts import render
import pymysql as mysql
from django.http import JsonResponse


def Actioncategoryinterface(request):
    try:
        rec = request.session['ADMIN_SES']
        return render(request, "categoryinterface.html", {'msg': ''})
    except:
        return render(request, "adminlogin.html", {'msg': ''})


def Actioncategorysubmit(request):
    cname = request.POST['cname']
    cdes = request.POST['cdes']
    file = request.FILES['cicon']
    try:
        dbe = mysql.connect(host="ec2-34-200-94-86.compute-1.amazonaws.com", port=5432,
                            user="ijcjrzlgenemkz", password='864dd0f35ea5241444ae1f9023989175a1adb30d3ffd8f170926b11e088aefb8', db="d1imieiq5pkn40")
        cmd = dbe.cursor()
        q = "INSERT INTO `category` (`categoryname`, `categorydescription`, `categoryicon`) VALUES ('{}', '{}', '{}')".format(
            cname, cdes, file.name)
        cmd.execute(q)
        dbe.commit()
        dbe.close()
        # upload files
        f = open('C:/Users/Aman Gupta/musicvideo/asset/' + file.name, 'wb')
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        return render(request, "categoryinterface.html", {'msg': 'Record Submitted'})
    except Exception as e:
        print(e)
        return render(request, "categoryinterface.html", {'msg': 'Fail to Submit Record'})


def ActioncategoryDisplayAll(request):
    try:
        rec = request.session['ADMIN_SES']
        try:
            dbe = mysql.connect(host="ec2-34-200-94-86.compute-1.amazonaws.com", port=5432,
                            user="ijcjrzlgenemkz", password='864dd0f35ea5241444ae1f9023989175a1adb30d3ffd8f170926b11e088aefb8', db="d1imieiq5pkn40")
            cmd = dbe.cursor()
            q = 'select * from category'
            cmd.execute(q)
            rows = cmd.fetchall()
            dbe.close()
            return render(request, "categorydisplayall.html", {'rows': rows})
        except Exception as e:
            print(e)
            return render(request, "categorydisplayall.html", {'rows': []})
    except:
        return render(request, "adminlogin.html", {'msg': ''})


def ActioncategoryDisplaybyid(request):
    try:
        cid = request.GET['cid']
        dbe = mysql.connect(host="ec2-34-200-94-86.compute-1.amazonaws.com", port=5432,
                            user="ijcjrzlgenemkz", password='864dd0f35ea5241444ae1f9023989175a1adb30d3ffd8f170926b11e088aefb8', db="d1imieiq5pkn40")
        cmd = dbe.cursor()
        q = 'select * from category where categoryid={}'.format(cid)
        cmd.execute(q)
        row = cmd.fetchone()
        dbe.close()
        return render(request, "categorydisplaybyid.html", {'row': row})
    except Exception as e:
        print(e)
        return render(request, "categorydisplaybyid.html", {'row': []})


def ActionCategoryEditDeleteSubmit(request):
    cid = request.POST['cid']
    cname = request.POST['cname']
    cdes = request.POST['cdes']
    btn = request.POST['btn']
    try:
        if(btn == "Edit"):
            dbe = mysql.connect(host="ec2-34-200-94-86.compute-1.amazonaws.com", port=5432,
                            user="ijcjrzlgenemkz", password='864dd0f35ea5241444ae1f9023989175a1adb30d3ffd8f170926b11e088aefb8', db="d1imieiq5pkn40")
            cmd = dbe.cursor()
            q = "update category set categoryname='{}',categorydescription='{}' where categoryid='{}'".format(
                cname, cdes, cid)
            cmd.execute(q)
            dbe.commit()
            dbe.close()
            return ActioncategoryDisplayAll(request)
        elif(btn == "Delete"):
            dbe = mysql.connect(host="ec2-34-200-94-86.compute-1.amazonaws.com", port=5432,
                            user="ijcjrzlgenemkz", password='864dd0f35ea5241444ae1f9023989175a1adb30d3ffd8f170926b11e088aefb8', db="d1imieiq5pkn40")
            cmd = dbe.cursor()
            q = "delete from category where categoryid='{}'".format(cid)
            cmd.execute(q)
            dbe.commit()
            dbe.close()
            return ActioncategoryDisplayAll(request)
    except Exception as e:
        print(e)
        return ActioncategoryDisplayAll(request)


def ActionEditCategoryPicture(request):
    cid = request.POST['cid']
    file = request.FILES['cicon']

    try:
        dbe = mysql.connect(host="ec2-34-200-94-86.compute-1.amazonaws.com", port=5432,
                            user="ijcjrzlgenemkz", password='864dd0f35ea5241444ae1f9023989175a1adb30d3ffd8f170926b11e088aefb8', db="d1imieiq5pkn40")
        cmd = dbe.cursor()
        q = "update category set categoryicon='{}' where categoryid={}".format(
            file.name, cid)
        cmd.execute(q)
        dbe.commit()
        dbe.close()
        f = open('C:/Users/Aman Gupta/musicvideo/asset/' + file.name, "wb")
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        return ActioncategoryDisplayAll(request)
    except Exception as e:
        print(e)
        return ActioncategoryDisplayAll(request)


def ActionDisplayJSON(request):
    try:
        dbe = mysql.connect(host="ec2-34-200-94-86.compute-1.amazonaws.com", port=5432,
                            user="ijcjrzlgenemkz", password='864dd0f35ea5241444ae1f9023989175a1adb30d3ffd8f170926b11e088aefb8', db="d1imieiq5pkn40")
        cmd = dbe.cursor()
        q = "select * from category"
        cmd.execute(q)
        rows = cmd.fetchall()
        print(type(rows))
        # print(rows)
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({})
