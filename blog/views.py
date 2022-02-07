from django.core.cache import cache
cache.clear() #キャッシュクリア

from django.shortcuts import render #ページ遷移用
from . import sleep

import cairo #モンドリアン風画像作成用
import random
import cv2 #明度変更用

import datetime #ログイン日記録用

# the size of the image
IMAGE_WIDTH = 500
IMAGE_HEIGHT = 500
# the size of the tile grid
MAP_WIDTH = 50
MAP_HEIGHT = 50
# the size of each tile
TILE_SIZE = 10
#MAX_LINES = 10
#MIN_LINES = 8
MAX_RECTS = 8
MIN_RECTS = 6
tiles = {}
#colors (0,white),(1,black),(2,red),(3,yellow)(4,blue)

# Create your views here.

#ログインID/Passを複数の関数で使用
ID = 'ID'
Pass = 'Pass'

#ログイン
def login(request):
    # POST
    if request.method == 'POST':
        #記入されたID/Passを取得
        userid = request.POST.get('userid')
        password = request.POST.get('password')

        #送信ボタンが押されたとき
        if 'buttom' in request.POST:
            if userid == 'sleep' and password == 'sleep':
                global ID
                global Pass
                ID = 'sleep'
                Pass = 'sleep'
                return render(request, 'blog/choice.html', {})

            for i in range(1, 15):
                #ID/Passが一致したときログイン、主観評価記録用にページ遷移
                if userid == 'sleep%d' %i and password == 'sleep%d' %i:
                    global ID
                    global Pass
                    ID = 'sleep%d' %i
                    Pass = 'sleep%d' %i
                    return render(request, 'blog/choice.html', {})

            #ID/Passが間違えているときページ遷移しない
            return render(request, 'blog/login.html', {})
    else:
        return render(request, 'blog/login.html', {})

def choice(request):
    if request.method == 'POST':

        #主観評価送信された日時取得
        dt_now = str(datetime.datetime.now())
        #主観評価取得
        state = int(request.POST.get('syukan'))
        #ファイル記録用主観評価取得
        file_state =str(request.POST.get('syukan'))

        fp = open(r'C:\Users\tmset\djangogirls\static\file.txt', 'a') #ファイル書き込み
        fp.write(dt_now) #アクセス時刻を記録
        fp.write('\n')
        fp.write(ID) #IDを記録
        fp.write('\n')
        fp.write(file_state) #主観評価を記録
        fp.write('\n')
        fp.close()

        #アカウントごとの睡眠効率を取得
        if ID == 'sleep1' and Pass == 'sleep1':
            sleepEfficiency = sleep1.sleepEfficiency
        elif ID == 'sleep2' and Pass == 'sleep2':
            sleepEfficiency = sleep2.sleepEfficiency
        elif ID == 'sleep3' and Pass == 'sleep3':
            sleepEfficiency = sleep3.sleepEfficiency
        elif ID == 'sleep4' and Pass == 'sleep4':
            sleepEfficiency = sleep4.sleepEfficiency
        elif ID == 'sleep5' and Pass == 'sleep5':
            sleepEfficiency = sleep5.sleepEfficiency
        elif ID == 'sleep6' and Pass == 'sleep6':
            sleepEfficiency = sleep6.sleepEfficiency
        elif ID == 'sleep7' and Pass == 'sleep7':
            sleepEfficiency = sleep7.sleepEfficiency
        elif ID == 'sleep8' and Pass == 'sleep8':
            sleepEfficiency = sleep8.sleepEfficiency
        elif ID == 'sleep9' and Pass == 'sleep9':
            sleepEfficiency = sleep9.sleepEfficiency
        elif ID == 'sleep10' and Pass == 'sleep10':
            sleepEfficiency = sleep10.sleepEfficiency
        elif ID == 'sleep11' and Pass == 'sleep11':
            sleepEfficiency = sleep11.sleepEfficiency
        elif ID == 'sleep12' and Pass == 'sleep12':
            sleepEfficiency = sleep12.sleepEfficiency
        elif ID == 'sleep13' and Pass == 'sleep13':
            sleepEfficiency = sleep13.sleepEfficiency
        elif ID == 'sleep14' and Pass == 'sleep14':
            sleepEfficiency = sleep14.sleepEfficiency
        elif ID == 'sleep15' and Pass == 'sleep15':
            sleepEfficiency = sleep15.sleepEfficiency
        elif ID == 'sleep' and Pass == 'sleep':
            sleepEfficiency = sleep.sleepEfficiency

        #時々sleepEfficiencyが空になるバグがあるので、その場合エラー画面に遷移
        try:
            sleepEfficiency = sleepEfficiency
        except UnboundLocalError:
            return render(request,'blog/retry.html',{})

        #日付が変わってからまだ寝ていないときもエラー画面に繊維
        if sleepEfficiency == 0:
            return render(request,'blog/nodata.html',{})

        #送信ボタンが押されたとき
        if 'buttom' in request.POST:
            #主観評価と客観評価のズレ、ページ遷移用変数を設定
            if state==1 or state=='１':
                if sleepEfficiency>=90:
                    gap = 0
                    stage = 1
                elif sleepEfficiency<90 and sleepEfficiency>=85:
                    gap = 1
                    stage = 2
                elif sleepEfficiency<85:
                    gap = 2
                    stage = 3
            elif state==2 or state=='２':
                if sleepEfficiency>=90:
                    gap = 1
                    stage = 4
                elif sleepEfficiency<90 and sleepEfficiency>=85:
                    gap = 0
                    stage = 5
                elif sleepEfficiency<85:
                    gap = 1
                    stage = 6
            elif state==3 or state=='３':
                if sleepEfficiency>=90:
                    gap = 2
                    stage = 7
                elif sleepEfficiency<90 and sleepEfficiency>=85:
                    gap = 1
                    stage = 8
                elif sleepEfficiency<85:
                    gap = 0
                    stage = 9
            else:
                return render(request,'blog/choice.html',{})


            #ズレに応じたモンドリアン風画像のボーダー数選択
            if gap==0:
                MAX_LINES = 10
                MIN_LINES = 8
            elif gap==1:
                MAX_LINES = 16
                MIN_LINES = 14
            elif gap==2:
                MAX_LINES = 25
                MIN_LINES = 20

            #睡眠効率から明度算出
            Value = sleepEfficiency/100

            #モンドリアン風画像作成
            generate_tiles(MIN_LINES, MAX_LINES)
            draw_map()
            changeValue(Value)

            #ページ遷移
            #(outputA1～9:文章、outputB1～9:画像、outputC1～9:文章＋画像)
            for i in range(1, 16):
                if userid == 'sleep%d' %i and password == 'sleep%d' %i:
                    if stage==1:
                        return render(request,'blog/outputC1.html',{})
                    elif stage==2:
                        return render(request,'blog/outputC2.html',{})
                    elif stage==3:
                        return render(request,'blog/outputC3.html',{})
                    elif stage==4:
                        return render(request,'blog/outputC4.html',{})
                    elif stage==5:
                        return render(request,'blog/outputC5.html',{})
                    elif stage==6:
                        return render(request,'blog/outputC6.html',{})
                    elif stage==7:
                        return render(request,'blog/outputC7.html',{})
                    elif stage==8:
                        return render(request,'blog/outputC8.html',{})
                    elif stage==9:
                        return render(request,'blog/outputC9.html',{})

    else:
        return render(request,'blog/choice.html',{})

#なくてもいいかもしれない関数
def output(request):
    return render(request, 'blog/output.html', {})

#モンドリアン風画像の白紙作成
def generate_tiles(MIN_LINES, MAX_LINES):
    # build tile map
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            # set every tile to white
            tiles[x,y] = 0
    draw_lines(MIN_LINES, MAX_LINES)

#白紙にボーダー作成
def draw_lines(MIN_LINES, MAX_LINES):
    total_lines = random.randint(MIN_LINES,MAX_LINES)
    for h in range(int(total_lines/2)):
        y = random.randint(0,MAP_HEIGHT)
        for x in range(MAP_WIDTH):
            tiles[x,y] = 1
    for v in range(int(total_lines/2)):
        x = random.randint(0,MAP_WIDTH)
        for y in range(MAP_HEIGHT):
            tiles[x,y] = 1
    fill_rects()

#着色するマスを選択
def fill_rects():
    total_rects = random.randint(MIN_RECTS,MAX_RECTS)
    max_iters = 5
    for i in range(max_iters):
        for r in range(total_rects):
            x = random.randint(0,MAP_WIDTH-1)
            y = random.randint(0,MAP_HEIGHT-1)
            if tiles[x,y] == 0:
                color = random.randint(2,4)
                flood_recursion(x,y,0,color)

#着色
def flood_recursion(x,y,start_color,update_color):
    width = MAP_WIDTH
    height = MAP_HEIGHT
    if tiles[x,y] != start_color:
        return
    elif tiles[x,y] == update_color:
        return
    else:
        tiles[x,y] = update_color
        neighbors = [(x-1,y),(x+1,y),(x-1,y-1),(x+1,y+1),(x-1,y+1),(x+1,y-1),(x,y-1),(x,y+1)]
        for n in neighbors:
            if 0 <= n[0] <= width-1 and 0 <= n[1] <= height-1:
                flood_recursion(n[0],n[1],start_color,update_color)

#数値による着色をRGBに変換し画像保存
def draw_map():
    # draw tile map using pycairo
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, IMAGE_WIDTH, IMAGE_HEIGHT)
    ctx = cairo.Context(surface)
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            size = TILE_SIZE
            ctx.rectangle(x*size,y*size,x+size,y+size)
            if tiles[x,y] == 0:
                ctx.set_source_rgb(1,1,1)
            elif tiles[x,y] == 1:
                ctx.set_source_rgb(0,0,0)
            elif tiles[x,y] == 2:
                ctx.set_source_rgb(1,0,0)
            elif tiles[x,y] == 3:
                ctx.set_source_rgb(1,1,0)
            else:
                ctx.set_source_rgb(0,0,1)
            ctx.fill()
    surface.write_to_png(r'C:\Users\tmset\djangogirls\static\mondrian.png')

#帆陣された画像を睡眠効率に応じて明度変更し画像保存
def changeValue(Value):
    img = cv2.imread(r'C:\Users\tmset\djangogirls\static\mondrian.png')  # 画像の読み出し
    img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)  # 色空間をBGRからHSVに変換
    s_magnification = 1  # 彩度(Saturation)の倍率
    v_magnification = Value # 明度(Value)の倍率

    img_hsv[:,:,(1)] = img_hsv[:,:,(1)]*s_magnification  # 彩度の計算
    img_hsv[:,:,(2)] = img_hsv[:,:,(2)]*v_magnification  # 明度の計算
    img_bgr = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)  # 色空間をHSVからBGRに変換
    cv2.imwrite(r'C:\\Users\tmset\djangogirls\static\mondrian.jpg',img_bgr)  # 画像の保存
