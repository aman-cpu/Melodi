from django.shortcuts import render
import pymysql as mysql
from django.http import JsonResponse


def Actionsonginterface(request):
    try:
        rec = request.session['ADMIN_SES']
        return render(request, "songinterface.html", {'msg': ''})
    except:
        return render(request, "adminlogin.html", {'msg': ''})


def Actionsongsubmit(request):
    scid = request.POST['scid']
    title = request.POST['title']
    releaseyear = request.POST['releaseyear']
    status = request.POST['status']
    stype = request.POST['type']
    singers = request.POST['singers']
    directors = request.POST['directors']
    musiccompany = request.POST['musiccompany']
    lyrics = request.FILES['lyrics']
    poster = request.FILES['poster']
    try:
        dbe = mysql.connect(host="localhost", port=3306,
                            user="root", password='', db="music")
        cmd = dbe.cursor()
        q = "INSERT INTO `song` (`scategoryid`, `title`, `releaseyear`, `lyrics`,`status`,`type`,`singers`,`directors`,`musiccompany`,`poster`) VALUES ('{}', '{}', '{}', '{}','{}', '{}','{}', '{}','{}', '{}')".format(
            scid, title, releaseyear, lyrics.name, status, stype, singers, directors, musiccompany, poster.name)
        cmd.execute(q)
        dbe.commit()
        dbe.close()
        # upload files
        f = open('C:/Users/Aman Gupta/musicvideo/asset/' + poster.name, 'wb')
        for chunk in poster.chunks():
            f.write(chunk)
        f.close()
        lf = open('C:/Users/Aman Gupta/musicvideo/asset/' + lyrics.name, 'wb')
        for chunk in lyrics.chunks():
            lf.write(chunk)
        lf.close()
        return render(request, "songinterface.html", {'msg': 'Record Submitted'})
    except Exception as e:
        print(e)
        return render(request, "songinterface.html", {'msg': 'Fail to Submit Record'})


def ActionsongDisplayAll(request):
    try:
        rec = request.session['ADMIN_SES']
        try:
            dbe = mysql.connect(host="localhost", port=3306,
                                user="root", password='', db="music")
            cmd = dbe.cursor()
            q = 'select * from song'
            cmd.execute(q)
            rows = cmd.fetchall()
            dbe.close()
            return render(request, "songdisplayall.html", {'rows': rows})
        except Exception as e:
            print(e)
            return render(request, "songdisplayall.html", {'rows': []})
    except:
        return render(request, "adminlogin.html", {'msg': ''})


def ActionsongDisplaybyid(request):
    try:
        songid = request.GET['songid']
        dbe = mysql.connect(host="localhost", port=3306,
                            user="root", password='', db="music")
        cmd = dbe.cursor()
        q = "select S.*, (select SC.scategoryname from subcategory SC where SC.scategoryid=S.scategoryid) as scategoryname from song S where S.songid={}".format(songid)
        cmd.execute(q)
        row = cmd.fetchone()
        dbe.close()
        return render(request, "songdisplaybyid.html", {'row': row})
    except Exception as e:
        print(e)
        return render(request, "songdisplaybyid.html", {'row': []})


def ActionSongEditDeleteSubmit(request):
    songid = request.POST['songid']
    title = request.POST['title']
    releaseyear = request.POST['releaseyear']
    status = request.POST['status']
    stype = request.POST['type']
    singers = request.POST['singers']
    directors = request.POST['directors']
    musiccompany = request.POST['musiccompany']
    lyrics = request.FILES['lyrics']
    btn = request.POST['btn']
    try:
        if(btn == "Edit"):
            dbe = mysql.connect(host="localhost", port=3306,
                                user="root", password='', db="music")
            cmd = dbe.cursor()
            q = "update song set title='{}',releaseyear='{}',status='{}',type='{}',singers='{}',directors='{}',musiccompany='{}',lyrics='{}' where songid='{}'".format(
                title, releaseyear, status, stype, singers, directors, musiccompany,lyrics.name, songid)
            print(q)
            cmd.execute(q)
            dbe.commit()
            dbe.close()
            lf = open('C:/Users/Aman Gupta/musicvideo/asset/' + lyrics.name, "wb")
            for chunk in lyrics.chunks():
                lf.write(chunk)
            lf.close()
            return ActionsongDisplayAll(request)
        elif(btn == "Delete"):
            dbe = mysql.connect(host="localhost", port=3306,
                                user="root", password='', db="music")
            cmd = dbe.cursor()
            q = "delete from song where songid='{}'".format(songid)
            cmd.execute(q)
            dbe.commit()
            dbe.close()
            return ActionsongDisplayAll(request)
    except Exception as e:
        print(e)
        return ActionsongDisplayAll(request)


def ActionEditSongPicture(request):
    songid = request.POST['songid']
    poster = request.FILES['poster']

    try:
        dbe = mysql.connect(host="localhost", port=3306,
                            user="root", password='', db="music")
        cmd = dbe.cursor()
        q = "update song set poster='{}' where songid={}".format(
            poster.name, songid)
        cmd.execute(q)
        dbe.commit()
        dbe.close()
        f = open('C:/Users/Aman Gupta/musicvideo/asset/' + poster.name, "wb")
        for chunk in poster.chunks():
            f.write(chunk)
        f.close()
        return ActionsongDisplayAll(request)
    except Exception as e:
        print(e)
        return ActionsongDisplayAll(request)


def ActionDisplaySubCategoryJSON(request):
    try:
        cid = request.GET['cid']
        # print(cid)
        dbe = mysql.connect(host="localhost", port=3306,
                            user="root", password='', db="music")
        cmd = dbe.cursor()
        q = "select *  from subcategory where categoryid={}".format(cid)
        # print(q)
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()

        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({})
