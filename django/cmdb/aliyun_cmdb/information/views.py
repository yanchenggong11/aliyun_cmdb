from django.shortcuts import render,redirect,HttpResponse

from . import models
from aliyunAPI import getBalance
from aliyunAPI import rdsAPI
from aliyunAPI import ecsAPI

from .forms import ProjectEditForm

import json

# Create your views here.


def login(request):
    error_msg = ''
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        try:
            user = models.User.objects.get(username=u)
            if user.password == p:
                request.session['is_login'] = True
                request.session['username'] = u
                res = redirect('/index/')
                return res
            else:
                error_msg = '密码错误'
        except:
            error_msg = '%s 该用户不存在！！！' %u
        return render(request,'information/login.html',locals())


    return render(request, 'information/login.html',locals())

def auth(func):
    def inner(request,*args, **kwargs):
        is_login = request.session.get('is_login',None)
        if is_login:
            return func(request,*args, **kwargs)
        else:
            return redirect('/login/')
    return inner

@auth
def index(request):

    return render(request,'information/index.html')

@auth
def project_info(request):
    if request.method == 'POST':
        p_name = request.POST.get('p_name')
        ali_account = request.POST.get('ali_account')
        ali_secrts = request.POST.get('ali_secrt')
        ali_region = request.POST.get('ali_region')
        ali_keyid = request.POST.get('ali_keyid')
        ali_idsecrts = request.POST.get('ali_idsecrts')
        ali_contact = request.POST.get('ali_contact')
        p_status = request.POST.get('p_status')
        p_time = request.POST.get('p_time')

        models.ProjectInfo.objects.create(p_name=p_name,ali_account=ali_account,ali_secrts=ali_secrts,
                                  ali_keyid=ali_keyid,ali_keysecrt=ali_idsecrts,ali_region=ali_region,ali_contact=ali_contact,
                                  p_status=p_status,p_date=p_time)
        return redirect('/project_info/')

    project_list = models.ProjectInfo.objects.all()
    for project in project_list:
        project_balance = getBalance.getBalance(project.ali_keyid,project.ali_keysecrt).getbalance()
        if not project_balance:
            continue
        models.ProjectInfo.objects.filter(id=project.id).update(ali_balance=project_balance)
    project_info = models.ProjectInfo.objects.all()
    return render(request,'information/project_info.html',{"info":project_info})

@auth
def project_del(request,pk):
    models.ProjectInfo.objects.filter(id=pk).delete()
    return  redirect('/project_info/')

@auth
def project_edit(request,pk):
    data = models.ProjectInfo.objects.filter(id=pk).values('p_name','ali_account','ali_secrts',
                                                           'ali_keyid','ali_keysecrt','ali_region','ali_contact',
                                                           'p_status','p_date').first()
    if request.method == 'POST':
        edit_form = ProjectEditForm(request.POST)
        if edit_form.is_valid():
            models.ProjectInfo.objects.filter(id=pk).update(p_name=request.POST.get('p_name').strip(),ali_account=request.POST.get('ali_account').strip(),
                                                            ali_secrts=request.POST.get('ali_secrts').strip(),ali_keyid=request.POST.get('ali_keyid').strip(),
                                                            ali_keysecrt=request.POST.get('ali_keysecrt').strip(),ali_region=request.POST.get('ali_region').strip(),
                                                            ali_contact=request.POST.get('ali_contact').strip(),
                                                            p_status=request.POST.get('p_status').strip(),p_date=request.POST.get('p_date'))

        return redirect('/project_info/')

    else:
        edit_form = ProjectEditForm(data)
        return render(request, 'information/project_edit.html',{'edit_form': edit_form,'id':pk})

@auth
def  project_data(request,pk):
    project_info = models.ProjectInfo.objects.filter(id=pk).first()
    p_name = project_info.p_name
    ali_keyid = project_info.ali_keyid
    ali_keysecrt = project_info.ali_keysecrt
    ali_region = project_info.ali_region

    rds_zone = rdsAPI.checkZoneRdsID(ali_keyid, ali_keysecrt, regionID=ali_region)
    rds_instance = rds_zone.get_rds_id(p_name)
    print(rds_instance)
    if rds_instance:
        rds_obj = rdsAPI.operatingRds(ali_keyid, ali_keysecrt,rds_instance,regionID=ali_region)
        rds_info = rds_obj.instance_info()
        r_engine = rds_info['rds_engine']
        r_usage = int(rds_info['disk_usage'])
        r_totalusage = int(rds_info['total_storage'])
        r_memory = int(rds_info['rds_memory'])
        r_cpu = int(rds_info['rds_cpu'])
        r_expire = int(rds_info['expire_day'])

        isExists = models.RdsInfo.objects.filter(p_name=p_name)
        if isExists:
            models.RdsInfo.objects.filter(p_name=p_name).update(r_aid=rds_instance, r_engine=r_engine, r_usage=r_usage,
                                          r_totalusage=r_totalusage, r_memory=r_memory, r_cpu=r_cpu, r_expire=r_expire)
        else:
            models.RdsInfo.objects.create(p_name=p_name, r_aid=rds_instance, r_engine=r_engine, r_usage=r_usage,
                                          r_totalusage=r_totalusage, r_memory=r_memory, r_cpu=r_cpu, r_expire=r_expire)

    else:
        pass

    # 获取ecs相关信息
    ecs_obj = ecsAPI.EcsOperating(ali_keyid,ali_keysecrt,regionID=ali_region)
    ecs_info = ecs_obj.get_ecs_status()
    print(ecs_info)
    for ecs in ecs_info:
        instanceId = ecs["InstanceId"]
        instanceName = ecs["InstanceName"]
        cpu = ecs["Cpu"]
        memory = ecs["Memory"]
        pivIp = ecs["PubIp"]
        pubIp = ecs["PivIp"]
        status = ecs["Status"]
        expireTime = ecs["ExpiredTime"]

        if models.EcsInfo.objects.filter(instanceId=instanceId):
            models.EcsInfo.objects.filter(instanceId=instanceId).update(cpu=cpu,memory=memory,pivIp=pivIp,
                                                                        pubIp=pubIp,status=status,expireTime=expireTime)
        else:
            models.EcsInfo.objects.create(p_name=p_name,instanceId=instanceId,instanceName=instanceName,cpu=cpu,
                                          memory=memory,pivIp=pivIp,pubIp=pubIp,status=status,expireTime=expireTime)
    return redirect('/project_info/')

@auth
def rds_info(request):
    rds_info = models.RdsInfo.objects.all()
    return  render(request,'information/rds_info.html',{'info': rds_info})

@auth
def ecs_info(request):
    p_all = models.EcsInfo.objects.values("p_name").distinct()
    ecs_list = []
    for p in p_all:
        ecs_dict = {}
        ecs_dict["p_name"] = p["p_name"]
        ecs_dict["ali_region"] = models.ProjectInfo.objects.filter(p_name=p["p_name"]).values("ali_region").first()["ali_region"]
        ecs_dict["ecs_count"] = models.EcsInfo.objects.filter(p_name=p["p_name"]).count()
        ecs_list.append(ecs_dict)

    return render(request,'information/ecs_info.html',{"ecs_list": ecs_list})
@auth
def ecs_detail(request,p_name):
    ecs_info = models.EcsInfo.objects.filter(p_name=p_name)

    return  render(request,'information/ecs_detail.html',{'p_name': p_name,'ecs_info':ecs_info})

@auth
def ecs_start(request):
    instanceIds = request.GET.getlist('instanceIds',[])
    msg = {'status': True, 'msg':''}
    if instanceIds:
        p_name = models.EcsInfo.objects.filter(id=instanceIds[0]).values("p_name").first()["p_name"]
        ali_info = models.ProjectInfo.objects.filter(p_name=p_name).values("ali_region","ali_keyid","ali_keysecrt").first()
        ali_region = ali_info["ali_region"]
        ali_keyid = ali_info["ali_keyid"]
        ali_keysecrt = ali_info["ali_keysecrt"]
        for instance in instanceIds:
            instanceId = models.EcsInfo.objects.filter(id=instance).values("instanceId").first()["instanceId"]
            ecsobj = ecsAPI.EcsOperating(ali_keyid, ali_keysecrt, regionID=ali_region)
            ecsobj.start_instance(instanceId)
        msg['status'] = True
        msg['msg'] = "主机实例启动完成"
    else:
        msg['status'] = False
        msg['msg'] = "未选取相关的主机"
    return HttpResponse(json.dumps(msg))

@auth
def ecs_restart(request,pk):
    instanceIds = request.GET.getlist('instanceIds', [])
    msg = {'status': True, 'msg': ''}
    if instanceIds:
        p_name = models.EcsInfo.objects.filter(id=instanceIds[0]).values("p_name").first()["p_name"]
        ali_info = models.ProjectInfo.objects.filter(p_name=p_name).values("ali_region", "ali_keyid",
                                                                           "ali_keysecrt").first()
        ali_region = ali_info["ali_region"]
        ali_keyid = ali_info["ali_keyid"]
        ali_keysecrt = ali_info["ali_keysecrt"]
        for instance in instanceIds:
            instanceId = models.EcsInfo.objects.filter(id=instance).values("instanceId").first()["instanceId"]
            ecsobj = ecsAPI.EcsOperating(ali_keyid, ali_keysecrt, regionID=ali_region)
            ecsobj.restart_instance(instanceId)
        msg['status'] = True
        msg['msg'] = "主机实例已重启"
    else:
        msg['status'] = False
        msg['msg'] = "未选取相关的主机"
    return HttpResponse(json.dumps(msg))

@auth
def ecs_stop(request):
    instanceIds = request.GET.getlist('instanceIds', [])
    msg = {'status': True, 'msg': ''}
    if instanceIds:
        p_name = models.EcsInfo.objects.filter(id=instanceIds[0]).values("p_name").first()["p_name"]
        ali_info = models.ProjectInfo.objects.filter(p_name=p_name).values("ali_region", "ali_keyid",
                                                                           "ali_keysecrt").first()
        ali_region = ali_info["ali_region"]
        ali_keyid = ali_info["ali_keyid"]
        ali_keysecrt = ali_info["ali_keysecrt"]
        for instance in instanceIds:
            instanceId = models.EcsInfo.objects.filter(id=instance).values("instanceId").first()["instanceId"]
            ecsobj = ecsAPI.EcsOperating(ali_keyid, ali_keysecrt, regionID=ali_region)
            ecsobj.stop_instance(instanceId)
        msg['status'] = True
        msg['msg'] = "主机实例已关闭"
    else:
        msg['status'] = False
        msg['msg'] = "未选取相关的主机"
    return HttpResponse(json.dumps(msg))

@auth
def ecs_reset(request):
    instanceIds = request.POST.getlist('instanceIds', [])
    password = request.POST.get('password')
    msg = {'status': True, 'msg': ''}
    if instanceIds:
        p_name = models.EcsInfo.objects.filter(id=instanceIds[0]).values("p_name").first()["p_name"]
        ali_info = models.ProjectInfo.objects.filter(p_name=p_name).values("ali_region", "ali_keyid",
                                                                           "ali_keysecrt").first()
        ali_region = ali_info["ali_region"]
        ali_keyid = ali_info["ali_keyid"]
        ali_keysecrt = ali_info["ali_keysecrt"]
        for instance in instanceIds:
            instanceId = models.EcsInfo.objects.filter(id=instance).values("instanceId").first()["instanceId"]
            ecsobj = ecsAPI.EcsOperating(ali_keyid, ali_keysecrt, regionID=ali_region)
            ecsobj.reset_password(instanceId,password)
        msg['status'] = True
        msg['msg'] = "主机实例密码已重置，请重启实例"
    else:
        msg['status'] = False
        msg['msg'] = "未选取相关的主机"
    return HttpResponse(json.dumps(msg))


from .forms import MyForm

def form_test(request):
    if request.method == 'GET':
        obj = MyForm()
        return render(request,'test/form_test.html',{'form':obj})
    elif request.method == 'POST':
        obj = MyForm(request.POST, request.FILES)
        if obj.is_valid():
            values = obj.clean()
            print(values)
        else:
            errors = obj.errors
            print(errors)
        return render(request,'test/form_test.html',{'form':obj})
    else:
        return redirect('http://www.baidu.com')












