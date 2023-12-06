import asyncio
from typing import *
from bilibili_api import video
import json
import requests
import time
import json
import emoji
import random
import os
import libcrawl



bv_list = ['BV1mQ4y1x7a1', 'BV1gc411D7wG', 'BV1LC4y1c7Fz', 'BV1e94y1j7fe', 'BV1bN4y1e7rH', 'BV14b4y1K772', 'BV1N94y177m1', 'BV1Da4y1R7iR', 'BV14w411h77o', 'BV1Wu4y1g7fU', 'BV1XQ4y1G71z', 'BV1aH4y1C7Qd', 'BV1Zb4y1K7CE', 'BV1Vc411B7uT', 'BV1bC4y1A7mm', 'BV1ru4y1c7gt', 'BV1Ne411f76R', 'BV19a4y1o7Um', 'BV1Ke411f75k', 'BV1aH4y1C7E4', 'BV1964y1L7Db', 'BV1a94y1E7Tn', 'BV14G411q7sq', 'BV1dg4y1Z7Ms', 'BV1je411f7a4', 'BV1ib4y1K7uR', 'BV1ou4y1c7fX', 'BV13N411j77Q', 'BV1kC4y1c79L', 'BV1ZH4y117Y5', 'BV1fC4y1y7AP', 'BV1je411f7wH', 'BV19M411o7LB', 'BV1EN411L7B1', 'BV1vC4y197eA', 'BV1cj411L7ay', 'BV1hH4y1C7CQ', 'BV1CC4y1A7tq', 'BV1tH4y1C7Nu', 'BV1Eu4y1V7oi', 'BV1Hj41157YB', 'BV1Nw411h7zy', 'BV1t34y1c75t', 'BV1tw411b7A2', 'BV1Hw411h7DT', 'BV1LN4y1e7w4', 'BV18N4y1Y7ek', 'BV1h94y1E7yo', 'BV1bw411h7q5', 'BV1ag4y1f79j', 'BV1Nu4y1g7tn', 'BV17g4y1f7bU', 'BV1dc411Q7fq', 'BV1Wg4y1f7QV', 'BV1Gu4y1V7LL', 'BV1pN411L79L', 'BV1Yc411S71B', 'BV1Eu4y1V78p', 'BV14u4y137Zy', 'BV1su4y1V7wH', 'BV1Nu4y1V7H7', 'BV1EG411q7mq', 'BV1DN4y1Y78g', 'BV1a94y1E74X', 'BV1RC4y1A7Tg', 'BV17C4y1A7mg', 'BV1xH4y1C7RD', 'BV1sb4y1K7Rm', 'BV1zQ4y1x71w', 'BV1Jc411B7y1', 'BV16e411d7zG', 'BV12N4y1Y7it', 'BV1Gc411B7s1', 'BV1YG411v7mL', 'BV1vu4y1c7VM', 'BV1Jj41157Cy', 'BV1yu4y1c7Tn', 'BV1JC4y1c7UC', 'BV1uu4y1L7rg', 'BV1Hb4y1L7G5', 'BV1ZN4y1Y7AZ', 'BV1tc411B7n8', 'BV1QH4y1C7kY', 'BV1vj41157xq', 'BV1AQ4y1V79o', 'BV1WC4y1c74b', 'BV1rQ4y1x7oN', 'BV1iw41187M3', 'BV1uN4y1e7VP', 'BV1Gw411b7Xi', 'BV1QM411d7NH', 'BV1gb4y1L7sC', 'BV1w94y177yg', 'BV1c34y1c7ui', 'BV1Ug4y1f7pk', 'BV1Qc411q7Tj', 'BV1wG411v7Gs', 'BV1wM411d7Lf', 'BV1gC4y1R7TC', 'BV1nj41157e3', 'BV1R64y177sF', 'BV1ku4y1V7JV', 'BV1kb4y1K7Pg', 'BV11j411j7kG', 'BV1TN4y1e7vp', 'BV1xN4y127uj', 'BV1ZQ4y1x7xL', 'BV1Yw411h7Aq', 'BV1Kb4y1T7YH', 'BV1Su4y1c7Dd', 'BV16u4y1g72K', 'BV1sN411L734', 'BV1LC4y1c7RP', 'BV1Nu4y1c7kb', 'BV1F94y1J71L', 'BV1Pw411h7yn', 'BV1Mc411D7yc', 'BV12H4y1C7vH', 'BV1Eu4y1V76E', 'BV1xw411h7ZA', 'BV1oN4y1Y76y', 'BV18G411q7YY', 'BV1ZH4y117Hg', 'BV1we411o76E', 'BV1mj411j7iZ', 'BV1DN411L7JF', 'BV1aa4y1R77X', 'BV1Za4y1o7h7', 'BV1T34y1c7RG', 'BV1934y1F7ue', 'BV1ow41187DX', 'BV1Xu4y1c7HC', 'BV1C64y1L7Mc', 'BV15u4y1c7zp', 'BV1Q94y177uY', 'BV1gc411i7Tv', 'BV1Xu4y1V7Pn', 'BV1zQ4y1x7sk', 'BV1uu4y1g7qU', 'BV1iM411R7W8', 'BV1SN41177Pj', 'BV1se411Z7fV', 'BV1N34y1c7hG', 'BV1SM411o7Y6', 'BV1Nw411b7Ss', 'BV1iM411R753', 'BV1664y1L7Ji', 'BV1rC4y1A7me', 'BV1N64y1j72p', 'BV1QM411R7XP', 'BV17N411L7sQ', 'BV1Ba4y1R7hk', 'BV1XC4y1A7BU', 'BV1Ke411f7md', 'BV1nC4y1c7za', 'BV1Tj411L7hX', 'BV1re411Z7Ev', 'BV1Ge411f7qW', 'BV1eN4y1Y7uT', 'BV1YC4y1c7hX', 'BV1sb4y1K7kR', 'BV1Nw411h75B', 'BV1NN4y1e7he', 'BV1rb4y1K7YE', 'BV1pG411q7HV', 'BV1ie411d7kT', 'BV14w411h7kc', 'BV1YC4y1c7vb', 'BV1ye411Z7sG', 'BV1QG411e7XS', 'BV1fQ4y1x7ta', 'BV1Yg4y1f7gC', 'BV1KG411q7T4', 'BV1uG411q7yu', 'BV1Gu4y1V7PN', 'BV1xu4y1L7hN', 'BV1qj411573U', 'BV1ea4y1o73X', 'BV1cc411X7Mi', 'BV1pN411L7Kt', 'BV1sC4y1A7UW', 'BV18G411q75M', 'BV1nw411h7Cz', 'BV1XC4y1A7XL', 'BV1uw411h7Zy', 'BV17w411h7ai', 'BV1TH4y1y7um', 'BV1Bu4y1g7zk', 'BV19a4y1d7fq', 'BV1Mc411Q7mg', 'BV17j41157oS', 'BV12C4y1c78w', 'BV1jc411B7Ld', 'BV1oQ4y1x7fg', 'BV1EQ4y1V7r5', 'BV1MQ4y147QP', 'BV1jw411h7SZ', 'BV1SM411d7T4', 'BV1Zc411q7MS', 'BV1Eb4y1K74i', 'BV1x34y1c7tT', 'BV14C4y1A7WE', 'BV1SC4y1A75Y', 'BV1hu4y1g7JY', 'BV1kw411h7Ad', 'BV1SC4y1A7Hj', 'BV1sg4y1f7pW', 'BV19N4y1Y7Kw', 'BV1Xe411Z7qV', 'BV1Bj411j7vS', 'BV16w41187fx', 'BV1bN411L7NA', 'BV1Sj411579z', 'BV1w94y1E7LW', 'BV1MM411d7wY', 'BV1n64y1j7aB', 'BV1BN4y127D9', 'BV1eC4y1978f', 'BV1e64y1L7ah', 'BV1gw411h7Ts', 'BV1HM411d7pS', 'BV1hN4y1e77L', 'BV1vC4y1y7Aq', 'BV1mc411Q7zr', 'BV1e94y1E79Q', 'BV1D64y177Am', 'BV1uv411F7BR', 'BV1vu4y1c7iK', 'BV1pb4y1M7re', 'BV1cu4y1c75r', 'BV1oe411d7XD', 'BV1PM411d7xF', 'BV1pN411j7c1', 'BV16M411R7n3', 'BV1QC4y1A7pr', 'BV1Wb4y1L78z', 'BV1kN4y1Y79n', 'BV1Zc411q7n2', 'BV1EM411d7KL', 'BV1Zc411Q7qm', 'BV1TC4y117sz', 'BV1rb4y1K7pF', 'BV1Dj411L7Kp', 'BV1Cb4y1K7JF', 'BV1uM411d7kH', 'BV1Aa4y1o7Pe', 'BV1cg4y1f7m1', 'BV1tw411b7Y4', 'BV1Nw411N7Qc', 'BV1vw41187bF', 'BV15Q4y147i2', 'BV1VC4y1A7hm', 'BV16M411R7MT', 'BV1Ya4y1R7wQ', 'BV1kC4y1y7br', 'BV1ga4y1o7yT', 'BV1qN4y127CQ', 'BV1cN4y1e7Po', 'BV1fQ4y1s7vm', 'BV11H4y117f2', 'BV1T34y1c76h', 'BV1Zb4y1N7nP', 'BV15c411B7Eo', 'BV1Vj411j7sP', 'BV14e411Z7xj', 'BV1VG411v7J1', 'BV1tH4y1C7PS', 'BV1JH4y1C7KQ', 'BV1N64y1j7uL', 'BV1kc411Q7XW', 'BV1GC4y117ty', 'BV1LC4y1c7mv', 'BV1Z94y1E7UH', 'BV1ia4y1o7L5', 'BV1re411d7p9', 'BV1Va4y1o7xb', 'BV1Y64y1L7w6', 'BV1Hu4y1V7tg', 'BV1pC4y1c7fR', 'BV1xG411i7uP', 'BV16M411d7ct', 'BV1hu4y1V79X', 'BV1ea4y1o7Yh', 'BV1j34y1F74B', 'BV1fe411Z7Gx', 'BV1JH4y117k5', 'BV1sG411q7Z1', 'BV18G411q78w', 'BV1Gu4y1V7we', 'BV1ke411d7tz', 'BV1iN4y127MC', 'BV1Fj411j7Jr', 'BV1qM411R79o', 'BV1zM411R7AM', 'BV1tc411Q7da', 'BV1Ej41157H1', 'BV1YC4y1c76a', 'BV1bu4y1V7w5', 'BV1We411Z7ym', 'BV1xG411q7QX', 'BV1xG411q7ws', 'BV14e411Z7LP', 'BV1su4y1c7FA', 'BV1zj411j7yy', 'BV1ia4y1R7Qn', 'BV1JG411q7Zx', 'BV1pH4y1C7SR', 'BV1qC4y1A7iF', 'BV1pg4y1f7ij', 'BV11H4y1C7BC', 'BV11C4y197u8', 'BV1Ta4y1Z79B', 'BV1dj41157uX', 'BV1Bu4y1c7Yv', 'BV1tu4y13765', 'BV16N4y1Y7HW', 'BV1Bc411S7ac', 'BV1yC4y1A7ku', 'BV1Qa4y1o7sm', 'BV16N4y127Az', 'BV1T64y1j7KJ', 'BV11c411z72o', 'BV1A34y1c7ys', 'BV12N4y127M9', 'BV1Pg4y1f7FA', 'BV1Hc411Q7Eq', 'BV1Uc411Q7yR', 'BV1fN411L7L7', 'BV1xb4y1M7Nh', 'BV1Fu4y1L7ne', 'BV1rH4y117As', 'BV15M411Z7ct', 'BV1rN411L76Q', 'BV1jj41157JZ', 'BV1gw411h7di', 'BV1YN411L7Em', 'BV1uC4y117WQ', 'BV1N94y1J7WG', 'BV1Fc41167mC', 'BV1dM411o79z', 'BV1gj41157R3', 'BV1pG411q7Nm', 'BV13j4115771', 'BV1hN4y1Y7s7', 'BV17j41157eM', 'BV18c411Q7Fi', 'BV13C4y1R72M', 'BV1fG411i7vP', 'BV1dw411n7zg', 'BV13H4y117j9', 'BV1zc411B7DF', 'BV1K34y1c7S5', 'BV1UQ4y1x7ij', 'BV1A64y1j7o8', 'BV1X64y177oF', 'BV1h34y1c7U9', 'BV1hw41187n9', 'BV1UC4y1976y', 'BV1Wu4y1g7im', 'BV1734y1c77Q', 'BV1pu4y1V7UC', 'BV1Tu4y1V7ru', 'BV1w94y1E7rG', 'BV1Ka4y1Z7dd', 'BV15w411H7Fa', 'BV1364y1j78p', 'BV1dN4y1Y71k', 'BV1pC4y1c7CB', 'BV1va4y1R7F8', 'BV1cg4y1f7jP', 'BV1Gu4y1c7LF', 'BV1na4y1o7bh', 'BV1aC4y1c7gN', 'BV1sc411Q767', 'BV1Rg4y1Z7KN', 'BV1Hg4y1f7sD', 'BV1RC4y1A7Zr', 'BV1jG411v7YU', 'BV1We411Z78h', 'BV1Gu4y1L7RW', 'BV1vH4y117Fu', 'BV1rc411q7oK', 'BV1ec411Q7F8', 'BV1g64y1j7Bi', 'BV1YQ4y1t76g', 'BV1mu4y1G7Sn', 'BV1jj41157uX', 'BV1D94y177K7', 'BV1Xc411z7zh', 'BV1x94y1E77u', 'BV1rN411L7WH', 'BV1jC4y1c7Le', 'BV1jj411j7z5', 'BV1W64y1L7gP', 'BV1nC4y1A7n6', 'BV1He411Z7Qp', 'BV1Qc411Q7YW', 'BV1oc411q7v6', 'BV1RC4y1A7ps', 'BV1Vu4y1g7N3', 'BV1pw411b7Gz', 'BV1w94y1J7FT', 'BV1ge411f7BA', 'BV1Ac411B7y6', 'BV1aG411q7Kb', 'BV1qe411d77V', 'BV1AQ4y147H9', 'BV1H64y1L7QU', 'BV1cQ4y1x77H', 'BV1TC4y117fD', 'BV1gQ4y1x7Hn', 'BV19N4y127zQ', 'BV1Qa4y1o7JN', 'BV1UC4y1A7Mf', 'BV1Mj41157ZF', 'BV1tQ4y1V7Lr', 'BV1Yc411Q7S1', 'BV1jw411h7hQ', 'BV1UN4y1Y7Hv', 'BV15Q4y1x7rc', 'BV1dN41177nr', 'BV1Wa4y1f7WW', 'BV1yc411S75t', 'BV1Xe411Z7Ek', 'BV1cu4y1c7zg', 'BV19Q4y1x7nw', 'BV1Qa4y1o7so', 'BV1fQ4y1s7mL', 'BV1bb4y1K76a', 'BV1iM411R7uJ', 'BV1oN4y1Y7vS', 'BV1hc411q7x1', 'BV1pC4y197vo', 'BV1oQ4y1x7dU', 'BV1wu4y1c7Yr', 'BV1R64y1L7pD', 'BV1ib4y1K7HZ', 'BV1264y1L7q4', 'BV1AM411d7Ab', 'BV12u4y1V7De', 'BV1ta4y1o7uq', 'BV13Q4y147To', 'BV1Ba4y1o7s3', 'BV1E34y1c72G', 'BV1PQ4y147Wj', 'BV1Ha4y1f7ZT', 'BV1RM411R7Qa', 'BV1W94y1E7AH', 'BV1ub4y1K7yP', 'BV1eC4y1A7Xk', 'BV1zc411S71o', 'BV12c411Q7ux', 'BV1Uu4y1c7mh', 'BV1Gc411z7mu', 'BV1kQ4y1x7zK', 'BV1Ua4y1R7Bo', 'BV1au4y1g7X8', 'BV1Ze411Z7zt', 'BV1YN41177KS', 'BV1Ja4y1o7NE', 'BV1Re411Z7kd', 'BV1aj411j7mQ', 'BV1EC4y197ep', 'BV1xu4y1L7wb', 'BV16N411L7Ku', 'BV1Fa4y1o7tw', 'BV1SQ4y1x7Hn', 'BV1mc411Q7Yi', 'BV1Vg4y1f7qg', 'BV1xw411h7Cm', 'BV1Ka4y1o7hw', 'BV14w41187Xn', 'BV1KG411q7QJ', 'BV1jH4y117gg', 'BV1Uc411Q7ty', 'BV1Ac411X7Yg', 'BV1tc411B7bM', 'BV13G411q72a', 'BV1tc411B72b', 'BV14C4y197tK', 'BV18b4y1M78m', 'BV1ia4y1o78S', 'BV14c411q7ZE', 'BV1Ta4y1Z7gJ', 'BV1Tu4y1V7Ja', 'BV1xH4y1y7Kb', 'BV1tj411j72c', 'BV12H4y1C7U2', 'BV1Ea4y1o7Ld', 'BV1pb4y1K7gs', 'BV1cM411d7a8', 'BV1i64y1L7hD', 'BV1v64y1L7am', 'BV1eu4y1c7p2', 'BV1SN4y127Li', 'BV1Uu4y1c7fR', 'BV11b4y1K7A2', 'BV1dM411o7v4', 'BV1qc411B7j7', 'BV1nQ4y1x7vP', 'BV1z94y1E7k7', 'BV1D94y1E7u5', 'BV1xN411L76i', 'BV1sc411q75i', 'BV1E64y1j7xe', 'BV1gC4y1A7eG', 'BV1fw41187Pn', 'BV1yN411778P', 'BV1gM411d7n2', 'BV1Me411Z7EJ', 'BV1Xj411L7Jp', 'BV11N411L7Tw', 'BV1cc411B7P4', 'BV11C4y1y7jL', 'BV1S64y1L7HS', 'BV1xC4y1y7LJ', 'BV1pj411j7Fx', 'BV18H4y127a1', 'BV1RQ4y1x7hY', 'BV1MM411d7Q9', 'BV1H64y1L7ab', 'BV1RG411i7q2', 'BV1sw411h71H', 'BV1Eu4y1L7ht', 'BV1GM411d78L', 'BV1RG411i7wj', 'BV1he411Z7Uh', 'BV1ye411Z75G', 'BV1v64y177vm']


def build_json_batch(bv: str, output_path: str, cookie: str=''):
    comment_text_list = libcrawl.get_comment_text_list(bv, cookie)
    res_json = {
        'comments': comment_text_list
    }
    if not output_path:
        output_path = bv + '.json'
    # use UTF-8 encoding
    with open(output_path, 'a', encoding='utf-8') as file:
        json.dump(res_json, file, ensure_ascii=False)


def build_txt_batch(bv: str, output_path: str, cookie: str=''):
    add_video_comments_to_end_of_the_file(bv, output_path, cookie)


def add_video_comments_to_end_of_the_file(bv: str, output_path: str, cookie: str='', max_num: int=100):
    comment_text_list = libcrawl.get_comment_text_list(bv, cookie)
    # shuffle the list
    random.shuffle(comment_text_list)
    if not output_path:
        output_path = bv + '.txt'
    # use UTF-8 encoding
    with open(output_path, 'a', encoding='utf-8') as file:
        count = 0
        for comment_text in comment_text_list:
            if count >= max_num:
                break
            # remove '\n' in comment_text
            comment_text = comment_text.replace('\n', '')
            file.write(comment_text + '\n')
            count += 1



if __name__ == '__main__':
    for bv in bv_list:
        add_video_comments_to_end_of_the_file(bv, 'D:\Personal\Program\Comprehensive\Emoprobe\crawler\cache\comments5.txt')
        print(bv + ' done.')