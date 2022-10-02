# -*- coding: utf-8 -*-
import os
import json
import re
import subprocess
import traceback

import psutil
import httpx

javaVersion = ""
manualMaxMem = 0
speedList = {}
NUM_LETTER = re.compile("^(?!\d+$)[\da-zA-Z_]+$")
FIRST_LETTER = re.compile("^[a-zA-Z]")


def getMemory():
    print("正在获取内存信息。。。")
    mem = psutil.virtual_memory()
    maxMemory = float(mem.total) / 1024 / 1024 / 1024
    freeMemory = float(mem.free) / 1024 / 1024 / 1024
    print("您的电脑内存为%.2fGB，可用内存为%.2fGB" % (maxMemory, freeMemory))
    manualMaxMem = input("如您想手动配置内存，清输入内存大小（单位为MB)，否则请直接回车：")
    if manualMaxMem == "":
        print("您选择了自动配置内存")
        return 0
    elif manualMaxMem.isdecimal():
        print("您选择了手动配置内存，内存大小为%sMB" % manualMaxMem)
        return int(manualMaxMem)
    else:
        print("您输入的内存大小有误，将自动配置内存")
        return 0


"""def getJavaVersion():
    print("是否使用JAVA8启动游戏？如确定请输入8，否则直接按回车以使用java11（推荐）：")
    print("现在不让选了，强制使用java8")
    return "java8"
"""


def username_validation(username):
    if NUM_LETTER.search(username):
        if FIRST_LETTER.search(username):
            return "ok"
        else:
            print("用户名不合法，请重新输入")
            return "only_num_letter"
    else:
        print("用户名不合法，请重新输入")
        return "first_letter"


def speedTest():
    serverListTXT = httpx.get("https://mc.toho.red/serverlist.txt").read()
    serverList = eval(serverListTXT)
    print("正在寻找最优线路。。。")
    for i in serverList:
        print("正在测试%s线路。。。" % i)
        speed = int(float(httpx.get("http://%s:8080/average" % i).read().decode()))
        print("线路%s负载为%s" % (i, speed))
        speedList[i] = speed
    highestSpeed = min(speedList.values())
    highestSpeedLine = [k for k, v in speedList.items() if v == highestSpeed]
    print("最优线路为%s" % (highestSpeedLine[0]))
    return highestSpeedLine[0]


def start(java_version, username, maxMemory):
    try:
        line = speedTest()
        print("游戏启动中，请不要关闭启动器")
        dir = os.getcwd()
        if int(maxMemory) == 0:
            memory = int(psutil.virtual_memory().free / 1024 / 1024 * 0.8)
        else:
            memory = maxMemory
        with open("launch.bat", "w") as f:
            f.write(
                """"Java\\{java}\\bin\\java.exe" -XX:+UseG1GC -XX:-UseAdaptiveSizePolicy -XX:-OmitStackTraceInFastThrow -Dfml.ignoreInvalidMinecraftCertificates=True -Dfml.ignorePatchDiscrepancies=True -Dlog4j2.formatMsgNoLookups=true -XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump -Xmn256m -Xmx{memory}m "-Djava.library.path={path}\\.minecraft\\versions\\Akaihasu\\Akaihasu-natives" -cp "{path}\\.minecraft\\libraries\\com\\mojang\\patchy\\1.3.9\\patchy-1.3.9.jar;{path}\\.minecraft\\libraries\\oshi-project\\oshi-core\\1.1\\oshi-core-1.1.jar;{path}\\.minecraft\\libraries\\net\\java\\dev\\jna\\jna\\4.4.0\\jna-4.4.0.jar;{path}\\.minecraft\\libraries\\net\\java\\dev\\jna\\platform\\3.4.0\\platform-3.4.0.jar;{path}\\.minecraft\\libraries\\com\\ibm\\icu\\icu4j-core-mojang\\51.2\\icu4j-core-mojang-51.2.jar;{path}\\.minecraft\\libraries\\net\\sf\\jopt-simple\\jopt-simple\\5.0.3\\jopt-simple-5.0.3.jar;{path}\\.minecraft\\libraries\\com\\paulscode\\codecjorbis\\20101023\\codecjorbis-20101023.jar;{path}\\.minecraft\\libraries\\com\\paulscode\\codecwav\\20101023\\codecwav-20101023.jar;{path}\\.minecraft\\libraries\\com\\paulscode\\libraryjavasound\\20101123\\libraryjavasound-20101123.jar;{path}\\.minecraft\\libraries\\com\\paulscode\\librarylwjglopenal\\20100824\\librarylwjglopenal-20100824.jar;{path}\\.minecraft\\libraries\\com\\paulscode\\soundsystem\\20120107\\soundsystem-20120107.jar;{path}\\.minecraft\\libraries\\io\\netty\\netty-all\\4.1.9.Final\\netty-all-4.1.9.Final.jar;{path}\\.minecraft\\libraries\\com\\google\\guava\\guava\\21.0\\guava-21.0.jar;{path}\\.minecraft\\libraries\\org\\apache\\commons\\commons-lang3\\3.5\\commons-lang3-3.5.jar;{path}\\.minecraft\\libraries\\commons-io\\commons-io\\2.5\\commons-io-2.5.jar;{path}\\.minecraft\\libraries\\commons-codec\\commons-codec\\1.10\\commons-codec-1.10.jar;{path}\\.minecraft\\libraries\\net\\java\\jinput\\jinput\\2.0.5\\jinput-2.0.5.jar;{path}\\.minecraft\\libraries\\net\\java\\jutils\\jutils\\1.0.0\\jutils-1.0.0.jar;{path}\\.minecraft\\libraries\\com\\google\\code\\gson\\gson\\2.8.0\\gson-2.8.0.jar;{path}\\.minecraft\\libraries\\com\\mojang\\authlib\\1.5.25\\authlib-1.5.25.jar;{path}\\.minecraft\\libraries\\com\\mojang\\realms\\1.10.22\\realms-1.10.22.jar;{path}\\.minecraft\\libraries\\org\\apache\\commons\\commons-compress\\1.8.1\\commons-compress-1.8.1.jar;{path}\\.minecraft\\libraries\\org\\apache\\httpcomponents\\httpclient\\4.3.3\\httpclient-4.3.3.jar;{path}\\.minecraft\\libraries\\commons-logging\\commons-logging\\1.1.3\\commons-logging-1.1.3.jar;{path}\\.minecraft\\libraries\\org\\apache\\httpcomponents\\httpcore\\4.3.2\\httpcore-4.3.2.jar;{path}\\.minecraft\\libraries\\it\\unimi\\dsi\\fastutil\\7.1.0\\fastutil-7.1.0.jar;{path}\\.minecraft\\libraries\\org\\apache\\logging\\log4j\\log4j-api\\2.15.0\\log4j-api-2.15.0.jar;{path}\\.minecraft\\libraries\\org\\apache\\logging\\log4j\\log4j-core\\2.15.0\\log4j-core-2.15.0.jar;{path}\\.minecraft\\libraries\\org\\lwjgl\\lwjgl\\lwjgl\\2.9.4-nightly-20150209\\lwjgl-2.9.4-nightly-20150209.jar;{path}\\.minecraft\\libraries\\org\\lwjgl\\lwjgl\\lwjgl_util\\2.9.4-nightly-20150209\\lwjgl_util-2.9.4-nightly-20150209.jar;{path}\\.minecraft\\libraries\\com\\mojang\\text2speech\\1.10.3\\text2speech-1.10.3.jar;{path}\\.minecraft\\libraries\\net\\minecraft\\launchwrapper\\1.12\\launchwrapper-1.12.jar;{path}\\.minecraft\\libraries\\net\\minecraftforge\\forge\\1.12.2-14.23.5.2860\\forge-1.12.2-14.23.5.2860.jar;{path}\\.minecraft\\libraries\\org\\ow2\\asm\\asm-debug-all\\5.2\\asm-debug-all-5.2.jar;{path}\\.minecraft\\libraries\\org\\jline\\jline\\3.5.1\\jline-3.5.1.jar;{path}\\.minecraft\\libraries\\com\\typesafe\\akka\\akka-actor_2.11\\2.3.3\\akka-actor_2.11-2.3.3.jar;{path}\\.minecraft\\libraries\\com\\typesafe\\config\\1.2.1\\config-1.2.1.jar;{path}\\.minecraft\\libraries\\org\\scala-lang\\scala-actors-migration_2.11\\1.1.0\\scala-actors-migration_2.11-1.1.0.jar;{path}\\.minecraft\\libraries\\org\\scala-lang\\scala-compiler\\2.11.1\\scala-compiler-2.11.1.jar;{path}\\.minecraft\\libraries\\org\\scala-lang\\plugins\\scala-continuations-library_2.11\\1.0.2_mc\\scala-continuations-library_2.11-1.0.2_mc.jar;{path}\\.minecraft\\libraries\\org\\scala-lang\\plugins\\scala-continuations-plugin_2.11.1\\1.0.2_mc\\scala-continuations-plugin_2.11.1-1.0.2_mc.jar;{path}\\.minecraft\\libraries\\org\\scala-lang\\scala-library\\2.11.1\\scala-library-2.11.1.jar;{path}\\.minecraft\\libraries\\org\\scala-lang\\scala-parser-combinators_2.11\\1.0.1\\scala-parser-combinators_2.11-1.0.1.jar;{path}\\.minecraft\\libraries\\org\\scala-lang\\scala-reflect\\2.11.1\\scala-reflect-2.11.1.jar;{path}\\.minecraft\\libraries\\org\\scala-lang\\scala-swing_2.11\\1.0.1\\scala-swing_2.11-1.0.1.jar;{path}\\.minecraft\\libraries\\org\\scala-lang\\scala-xml_2.11\\1.0.2\\scala-xml_2.11-1.0.2.jar;{path}\\.minecraft\\libraries\\lzma\\lzma\\0.0.1\\lzma-0.0.1.jar;{path}\\.minecraft\\libraries\\java3d\\vecmath\\1.5.2\\vecmath-1.5.2.jar;{path}\\.minecraft\\libraries\\net\\sf\\trove4j\\trove4j\\3.0.3\\trove4j-3.0.3.jar;{path}\\.minecraft\\libraries\\optifine\\OptiFine\\1.12.2_HD_U_G5\\OptiFine-1.12.2_HD_U_G5.jar;{path}\\.minecraft\\libraries\\org\\apache\\maven\\maven-artifact\\3.5.3\\maven-artifact-3.5.3.jar;{path}\\.minecraft\\versions\\Akaihasu\\Akaihasu.jar" net.minecraft.launchwrapper.Launch --versionType PCL2 --username {name} --version Akaihasu --gameDir "{path}\\.minecraft" --assetsDir "{path}\\.minecraft\\assets" --assetIndex 1.12 --uuid 000000000000300B9CEA04EDF3245170 --accessToken 000000000000300B9CEA04EDF3245170 --userType Legacy --tweakClass net.minecraftforge.fml.common.launcher.FMLTweaker --versionType Forge --height 480 --width 854 --tweakClass optifine.OptiFineForgeTweaker -server {line} --port 25560""".format(
                    java=java_version, path=dir, name=username, line=line, memory=memory))
            f.close()
        subprocess.run("launch.bat", shell=True, check=True, capture_output=True)
    except:
        return traceback.format_exc()


def check_config_file():
    if os.path.exists("config.json"):
        print("读取配置文件成功")
        with open("config.json", "r", encoding='UTF-8') as f:
            config = json.load(f)
        maxMemory = config['maxMemory']
        username = config['username']
        java_version = config['javaVersion']
        return ["true", maxMemory, username, java_version]
    else:
        print("未找到配置文件，需要创建配置文件")
        return ["false"]


def create_config_file(java_version, max_memory, username):
    with open("config.json", "w", encoding='UTF-8') as f:
        config = {
            "javaVersion": java_version,
            "maxMemory": str(max_memory),
            "username": username
        }
        json.dump(config, f, indent=4)
    print("创建配置文件成功")
    return ["true"]


def change_max_memory(max_memory):
    with open("config.json", "r", encoding='UTF-8') as f:
        config = json.load(f)
    config["maxMemory"] = max_memory
    with open("config.json", "w", encoding='UTF-8') as f:
        json.dump(config, f, indent=4)
    print("修改最大内存成功")
    return ["true"]


def change_username(username):
    with open("config.json", "r", encoding='UTF-8') as f:
        config = json.load(f)
    config["username"] = username
    with open("config.json", "w", encoding='UTF-8') as f:
        json.dump(config, f, indent=4)
    print("修改用户名成功")
    return ["true"]
