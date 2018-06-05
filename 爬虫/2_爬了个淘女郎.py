# -*- coding: utf-8 -*-
import re
import urllib2,string
import urllib
import os
import sys
##解决中文编码错误问题，但会带来其他问题，不建议使用
##reload(sys)
##sys.setdefaultencoding('utf-8')

class Spider():
    #默认构造函数，调用类时会自动运行
    def __init__(self):
        self.UrlSite='https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'

    ##解析原始网页链接
    def GetPage(self,Page):
        ## ajax异步加载方式，这部分地址需要利用开发者工具寻找，即用户post内容
        suffix='&q&viewFlag=A&sortType=default&searchStyle=&searchRegion=city%3A&searchFansNum=&currentPage='+str(Page)+'&pageSize=100'
        FullUrl=self.UrlSite+suffix
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(FullUrl, headers = headers)   
        myResponse = urllib2.urlopen(req)
##        print myResponse.read()
        return myResponse.read().decode('gbk')

    ##获取需要的文本信息
    def GetContent(self,Page):
        regex='{"avatarUrl".*?city":"(.*?)","height":"(.*?)","identityUrl":"","modelUrl":"","realName":"(.*?)".*?"userId":(.*?),.*?"weight":"(.*?)"}'
        contents=re.findall(regex,self.GetPage(Page),re.S)
        itemlist=[]
        for item in contents:
##            print "城市：",item[0]
##            print "身高：",item[1],"cm"
##            print "姓名：",item[2]
##            print "ID：",item[3]
##            print "体重：",item[4],"kg"
##            print "-------------"
            itemlist.append([item[0],item[1],item[2],item[3],item[4]])
            ##未完待,
        return itemlist
    
    ##储存单张图片
    def SaveImg(self,imgurl,outpath,outname):
        try:
            imgResponse = urllib2.urlopen(imgurl)
            image=imgResponse.read()
            f=open(outpath+"\\"+outname+".jpg",'wb')
            f.write(image)
            f.close()
        except:
            print u"图片地址无效"
        
    ##保存个人信息    
    def SaveInfo(self,info,outpath,outname):
        filename=outpath+"\\"+outname+".txt"
        f=open(filename,'w+')
        print outpath+'\\'+outname+'.txt'
        f.write(info)
        f.close()
        
    ##保存单页所有淘女郎信息
    def SaveAll(self,Page):
        basedir="E:\\girls\\"+u"第"+str(Page)+u"页"+"\\"
       
        textinfo=self.GetContent(Page)
        for i in range(len(textinfo)):
            item=textinfo[i]
            print "城市：",item[0]
            print "身高：",item[1],"cm"
            print "姓名：",item[2]
            print "ID：",item[3]
            print "体重：",item[4],"kg"
            print"-------------"
            infostr=u"城市："+item[0]+"\n"+u"身高："+item[1]+"\n"+u"姓名："+item[2]+"\n"+u"ID："+item[3]+"\n"+u"体重："+item[4]
            name=item[2]
            ID=item[3]
            output_path=basedir+name
##            print output_path
            ##创建个人文件夹
            if os.path.exists(output_path)==False:
                os.makedirs(output_path)
            ##保存基本信息
            self.SaveInfo(infostr.encode('utf-8'),output_path,name)
            ##保存个人照片
            Imgurl='https://mm.taobao.com/self/aiShow.htm?spm=719.7763510.1998643336.'+str(i)+'.xKWaiQ&userId='+ID
##            req=urllib2.Request(Imgurl)
            try:
                response=urllib2.urlopen(Imgurl)
                response=response.read()
                images=re.findall('<img style=.*?src="(.*?)"/>',response,re.S)
                for m in range(len(images)):
                    if m<=10:
                        imgurl="http:"+images[m]
                        print u"正在保存第"+str(m+1)+u"张："
                        self.SaveImg(imgurl,output_path,str(m+1))
            except:
                print u"这波网页寻找失败咯。。"
            print "\n\n"

    ##保存指定页数的内容            
    def SaveMultiPages(self,pages):
        for i in range(11,pages):
            print u"开始爬取第"+str(i+1)+u"页淘女郎数据："
            self.SaveAll(i+1)
        print u"爬完收工!"
Spider=Spider()
Spider.SaveMultiPages(20)
