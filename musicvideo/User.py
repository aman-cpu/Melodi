from django.shortcuts import render
import pymysql as mysql
import ast
from django.http import JsonResponse


def ActionMainPage(request):
    try:
        dbe = mysql.connect(host="melodimusicapp.herokuapp.com", port=3306,
                            user="root", password='', db="music")
        cmd = dbe.cursor()
        q = 'select * from category'
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return render(request, "melodi/index.html", {'rows': rows})
    except:
        return render(request, "melodi/index.html", {'rows': []})


def FetchAllRecord(q):
    try:
        dbe = mysql.connect(host="localhost", port=3306,
                            user="root", password='', db="music")
        cmd = dbe.cursor()
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return rows
    except Exception as e:
        print(e)
        return []


def ActionCategoryPage(request):
    try:
        q = "select *  from category"
        rows = FetchAllRecord(q)
        q = "select *  from song"
        srows = FetchAllRecord(q)
        return render(request, "melodi/category.html", {'rows': rows, 'srows': srows})
    except:
        return render(request, "melodi/category.html", {'rows': [], 'srows': []})


def ActionSubcategoryPage(request):
    cid = request.GET['cid']
    try:
        q = "select *  from subcategory where categoryid={}".format(cid)
        rows = FetchAllRecord(q)
        return render(request, "melodi/subcategory.html", {'rows': rows})
    except:
        return render(request, "melodi/subcategory.html", {'rows': []})

def ActionArtistPage(request):
    sc= request.GET["scid"]
    try:
        print(sc)
        sc=ast.literal_eval(sc)
        q = "select *  from song where scategoryid={}".format(sc[0])
        print(q)
        rows = FetchAllRecord(q)
        return render(request, "melodi/artist.html", {'rows': rows,'sc':sc})
    except:
        return render(request, "melodi/artist.html", {'rows': [],'sc':sc})


def ActionPlayListPage(request):
    try:
        q = "select *  from category"
        rows = FetchAllRecord(q)
        q = "select *  from subcategory"
        srows = FetchAllRecord(q)
        return render(request, "melodi/playlist.html", {'rows': rows, 'srows': srows})
    except:
        return render(request, "melodi/playlist.html", {'rows': [], 'srows': []})

def ActionSearchSongPage(request):
    try:
        q="select * from song"
        rows = FetchAllRecord(q)
        return render(request, "melodi/searchsong.html", {'rows': rows})
    except:
        return render(request, "melodi/searchsong.html", {'rows': []})

def ActionSearchSongJson(request):
    try:
        pat=request.GET['pat']
        q="select *  from song where title like '%{}%'".format(pat)
        print(q)
        rows = FetchAllRecord(q)
        return JsonResponse(rows,safe=False)
    except:
        return JsonResponse([],safe=False)

def ActionPlaySong(request):
    try:
        sg= request.GET["sg"]
        print("xxxxxx",sg)
        sg=sg.split(",")
        print(sg)
        q = "select *  from song where songid={0}".format(sg[0])
        print(q)
        rows = FetchAllRecord(q)
        print(rows)
        return render(request, "melodi/playsong.html", {'row': rows[0]})
    except Exception as e:
        print("Error",e)
        return render(request, "melodi/playsong.html", {'row': []})        


