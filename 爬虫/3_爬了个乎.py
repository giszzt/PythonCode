# -*- coding: utf-8 -*-   
import os
import json
from scrapy import Spider,Request
import urllib2
import re
##------爬取知乎某个用户的全部相关信息-----##

##def BasePage_Content():
##    start_url='https://www.zhihu.com/api/v4/members/tim57414473/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
##    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
##    ##设置使用浏览器配置，以及认证内容
##    headers = { 'User-Agent' : user_agent ,'authorization':'Bearer Mi4xWkswdEFBQUFBQUFBZ0lLcUVZZG1EQmNBQUFCaEFsVk56Y1h2V2dDN013Z3BKd2Z4blE3UDFsV1BKWGdiejhRd1BR|1510111181|a6da0f7b205b4b32b3406755f33a515fa3b58d72'}
##    req = urllib2.Request(start_url, headers = headers)
##    myResponse = urllib2.urlopen(req)
##    content=myResponse.read()
##    c=json.loads(content)
##    data=c['data']##获取当前键所对应的值
##    return data
##    getInfo=re.findall('"answer_count": (.*?),.*?"headline": "(.*?)", "url_token": "(.*?)",.*?, "type": "people", "name": "(.*?)", "url":.*?"gender": (.*?), "is_advertiser"',content,re.S)
##    for item in getInfo:
##        print u"个性签名：",item[1].decode('unicode_escape')##如果本就是中文unicode编码，用escape可正常显示


def Get_JsonContent(input_url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'##设置使用浏览器配置，以及认证内容
    ##这个认证码很重要，要仔细检查
    headers = { 'User-Agent' : user_agent ,'authorization':'。。。。。。'}
    req = urllib2.Request(input_url, headers = headers)
    myResponse = urllib2.urlopen(req)##打开页面
    content=myResponse.read()##读取页面
    con=json.loads(content)
    page=con['paging']
    data=con['data']##获取当前键所对应的值
    return page,data
    
def Get_Answers(Url_Token):
    answer_url='https://www.zhihu.com/api/v4/members/'+Url_Token+'/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,collapsed_by,suggest_edit,comment_count,can_comment,content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,question,excerpt,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp,upvoted_followees;data[*].author.badge[?(type=best_answerer)].topics&offset=0&limit=20&sort_by=created'
    page,answers=Get_JsonContent(answer_url)
    if page['totals']==0:
        print "这个人没有回答过问题。"
    else:
        print "<"+answers[0]['author']['name']+">"+u"共回答了"+str(page['totals'])+u"个问题"
        ##获取前一百个回答，如果有的话
        for n in range(0,100,20):
            answer_url='https://www.zhihu.com/api/v4/members/'+Url_Token+'/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,collapsed_by,suggest_edit,comment_count,can_comment,content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,question,excerpt,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp,upvoted_followees;data[*].author.badge[?(type=best_answerer)].topics&offset='+str(n)+'&limit=20&sort_by=created'
            page,answers=Get_JsonContent(answer_url)
            if len(answers)!=0:
                contentList=[]
                ##每个回答详细信息
                for i in range(len(answers)):
                   Question=answers[i]['question']['title']
                   Answer=answers[i]['content']
                   Voteup=answers[i]['voteup_count']
                   comments=answers[i]['comment_count']
                   print "第"+str(n+i+1)+"个回答："
                   print Question
                   print "有"+str(Voteup)+"个人给他点赞了，"+str(comments)+"个人评论了他的答案"
                   Answer_Edited=Format_Edition(Answer)
                   single_info=u"第"+str(n+i+1)+u"个回答：\n"+Question
                   ##设置输出路径
                   outpath=u'E:\Python代码\爬虫应用'
                   outname=u'answers'
                   Save_Textfile(single_info.encode('utf-8'),outpath,outname)
                   for i in Answer_Edited:
                      Save_Textfile(i.encode('utf-8'),outpath,outname)
##                   Save_Textfile("\n--------",outpath,outname)
                   if Voteup>100:
                       print u"真是牛逼啊"
                   print "-----------\n"
            else:
                 print"到头了"

def Get_Articles(Url_Token):
    Article_url='https://www.zhihu.com/api/v4/members/'+Url_Token+'/articles?include=data[*].comment_count,can_comment,comment_permission,admin_closed_comment,content,voteup_count,created,updated,upvoted_followees,voting,review_info;data[*].author.badge[?(type=best_answerer)].topics&offset=20&limit=20&sort_by=created'
    page,articles=Get_JsonContent(Article_url)
    if page['totals']==0:
        print "这个人没有发表过文章。"
    else:
        print "<"+articles[0]['author']['name']+">"+u"共发表了"+str(page['totals'])+u"篇文章"
        ##获取前一百篇文章回答，如果有的话
        for n in range(0,100,20):
            article_url='https://www.zhihu.com/api/v4/members/'+Url_Token+'/articles?include=data[*].comment_count,can_comment,comment_permission,admin_closed_comment,content,voteup_count,created,updated,upvoted_followees,voting,review_info;data[*].author.badge[?(type=best_answerer)].topics&offset='+str(n)+'&limit=20&sort_by=created'
            page,article=Get_JsonContent(article_url)
            if len(article)!=0:                               
                ##每篇文章的详细信息
                for i in range(len(article)):
                   Title=article[i]['title']
                   content=article[i]['content']
                   Voteup=article[i]['voteup_count']
                   comments=article[i]['comment_count']
                   print "第"+str(n+i+1)+"篇文章："
                   print Title
                   print "有"+str(Voteup)+"个人给他点赞了，"+str(comments)+"个人评论了他的文章"
                   if Voteup>500:
                       print u"点赞的好多啊"
                   print "-----------\n"
            else:
                 break

def Get_Followers(Url_Token):
    Follower_url='https://www.zhihu.com/api/v4/members/'+Url_Token+'/followers?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=20&limit=20'
    page,followers=Get_JsonContent(Follower_url)
    if page['totals']==0:
        print "没有人关注他啊！"
    else:
        print u"共有"+str(page['totals'])+u"关注了她"
        ##获取前一百个关注者，如果有的话
        for n in range(0,100,20):
            Follower_url='https://www.zhihu.com/api/v4/members/'+Url_Token+'/followers?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset='+str(n)+'&limit=20'
            page,followers=Get_JsonContent(Follower_url)
            if len(followers)!=0:                                
                ##每个关注者的详细信息
                for i in range(len(followers)):
                   NickName=followers[i]['name']##昵称
                   Headline=followers[i]['headline']##个性签名
                   Gender=followers[i]['gender']##性别，1为男，-1为女
                   if Gender==1:
                      sex="是个男孩儿"
                   if Gender==-1:
                      sex="是个女孩儿"
                   if Gender==0:
                      sex="他不想告诉你是男是女--！" 
                   answers=followers[i]['answer_count']##回答数
                   Url_token=followers[i]['url_token']##个人链接id
                   follower=followers[i]['follower_count']##关注量
                   print "第"+str(n+i+1)+"个关注者："
                   print NickName
                   print Headline
                   print sex
                   print "有"+str(answers)+"个回答！"
                   print "有"+str(follower)+"个关注者！"
                   if follower>500:
                       print u"这人可以的"
                   print "-----------\n"
            else:
                 break

def Get_Following(Url_Token):
    Followee_url='https://www.zhihu.com/api/v4/members/'+Url_Token+'/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=0&limit=20'
    page,followee=Get_JsonContent(Followee_url)
    if page['totals']==0:
        print "他毛都没关注一个！"
    else:
        print u"他关注了"+str(page['totals'])+u"个人"
        ##获取关注的前一百个人，如果有的话
        for n in range(0,100,20):
##            a ='https://www.zhihu.com/api/v4/members/Retsu/activities?limit=10&after_id=1511581851&desktop=True'
            Followee_url='https://www.zhihu.com/api/v4/members/'+Url_Token+'/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset='+str(n)+'&limit=20'
            page,followees=Get_JsonContent(Followee_url)
            if len(followees)!=0:                                
                ##每个关注者的详细信息
                for i in range(len(followees)):
                   NickName=followees[i]['name']##昵称
                   Headline=followees[i]['headline']##个性签名
                   Gender=followees[i]['gender']##性别，1为男，-1为女
                   if Gender==1:
                      sex="是个男孩儿"
                   if Gender==-1:
                      sex="是个女孩儿"
                   if Gender==0:
                      sex="他不想告诉你是男是女--！" 
                   answers=followees[i]['answer_count']##回答数
                   Url_token=followees[i]['url_token']##个人链接id
                   follower=followees[i]['follower_count']##关注量
                   print "关注的第"+str(n+i+1)+"人："
                   print NickName
                   print Headline
                   print sex
                   print "有"+str(answers)+"个回答！"
                   print "有"+str(follower)+"个关注者！"
                   if follower>500:
                       print u"这人可以的"
                   print "-----------\n"
            else:
                 print "已搜索到最后一页，再见。"
                 break

def Get_Questions(Url_Token):
    Questions_url='https://www.zhihu.com/api/v4/members/'+Url_Token+'/questions?include=data[*].created,answer_count,follower_count,author,admin_closed_comment&offset=0&limit=20'
    page,Questions=Get_JsonContent(Questions_url)
    if len(Questions)!=0:
        contentList=[]
        for i in range(len(Questions)):
            Title=Questions[i]['title']
            print "第"+str(i+1)+"个问题是："
            print Title

            single_info="第"+str(i+1)+"个问题是：\n"+Title
            contentList.append(single_info)
        outpath='E:\Python代码\爬虫代码'
        outname='Questions'
        Save_Textfile(contentList,outpath,outname)
    else:
        print "他没提过问题"
       

def Save_Textfile(text,outpath,outname):
    filename=outpath+"\\"+outname+".txt"
    f=open(filename,'a+')
##    print outpath+'\\'+outname+'.txt'
    f.write(text+"\n")
    f.close()

def Format_Edition(Info_Content):
    Info_Wanted=re.findall('<p>(.*?)</p>',Info_Content,re.S)
    return Info_Wanted
    
if __name__=="__main__":
    ##个人主页id标识
    Url_Token="tim57414473" 
#    Get_Questions(Url_Token)##看看他提了几个问题
    Get_Answers(Url_Token)##看看他有多少回答                
#    Get_Articles(Url_Token)##看看他发了几篇文章
#    Get_Followers(Url_Token)##看看有多少人关注了她
#    Get_Following(Url_Token)##看看他关注了多少人
