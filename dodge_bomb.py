import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, +5), pg.K_LEFT: (-5, 0), pg.K_RIGHT: (+5, 0)}  # 移動量の辞書
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数：無し
    戻り値：タプル（爆弾の大きさのSurfaceのリスト, 縦横の加速）
    時間とともに爆弾が拡大、加速する
    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


def gameover(screen: pg.Surface) -> None:
    """
    引数：screen
    戻り値：無し
    爆弾に当たった時にGame Overの画面をscreenにblitする
    """
    gameover_img = pg.Surface((1100, 650))
    gameover_img.fill((0, 0, 0))
    gameover_img.get_alpha()
    gameover_txt = pg.font.Font(None, 100)
    txt = gameover_txt.render("Game Over", True, (255, 255, 255))
    gameover_img.blit(txt, [360, 300])
    koukaton_img = pg.image.load("fig/8.png")
    gameover_img.blit(koukaton_img, [310, 300])
    gameover_img.blit(koukaton_img, [740, 300])
    screen.blit(gameover_img, [0, 0])
    pg.display.update()
    time.sleep(5)


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（横方向判定結果, 縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko = True
    tate = True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    bb_img = pg.Surface((20, 20))  # 縦横20の正方形
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 正方形に赤色の円を描画
    bb_img.set_colorkey((0, 0, 0))  # Surfaceの黒い部分の透過
    bb_rct = bb_img.get_rect()  # bb_imgをbb_rctに
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 画面内でランダムにbb_imgを設置
    vx = +5  # bb_imgの縦の速度
    vy = +5  # bb_imgの横の速度
    bb_imgs, bb_accs = init_bb_imgs()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):  # 爆弾に当たった時
            gameover(screen)  # ゲームオーバーの表示
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 左右の移動
                sum_mv[1] += mv[1]  # 上下の移動
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        avx = vx*bb_accs[min(tmr//500, 9)]  # 時間経過による爆弾の横の速度
        avy = vy*bb_accs[min(tmr//500, 9)]  # 時間経過による爆弾の縦の速度
        bb_img = bb_imgs[min(tmr//500, 9)]  # 時間経過による爆弾の大きさ
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, avy)  # bb_rctの移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *=-1
        screen.blit(bb_img, bb_rct)  # bb_imgをbb_rctにblitし動かせるように
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
