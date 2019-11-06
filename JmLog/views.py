from django.shortcuts import render
from .pak import SFTP
from django.conf import settings
import logging
import os
from django.views.generic import ListView, View, DetailView, CreateView, UpdateView
from JmLog import settings
from .kubernetes import K8sApi

def jm_log(request):
    if request.method == 'POST':
        spt_name = request.POST.get('script_name')
        spt_args = request.POST.get('script_args')
        command = 'sh' + ' ' + spt_name + ' ' + spt_args
        try:
            sftp = SFTP('117.50.11.196', 22, 'root', key_file=settings.KEY_FILE)
            data = sftp.execCommand(command)
            sftp = SFTP('117.50.11.196', 22, 'root', key_file=settings.KEY_FILE)
            download_file_path = os.path.join(settings.MEDIA_ROOT, 'log_files',)
            response = sftp.download_file(data[0], download_file_path)
            return response
        except Exception as e:
            logging.getLogger().error(e)
        finally:
            pass
    sftp = SFTP('117.50.11.196', 22, 'root', key_file=settings.KEY_FILE)
    #脚本文件所在目录
    data = sftp.execCommand('ls /root')
    return render(request,'index.html',{'data':data})


class K8sPodListView(View):

    def get(self, request):
        obj = K8sApi()
        ret = obj.get_pod_list()
        data = {}
        for i in ret.items:
            data[i.metadata.name] = {"ip": i.status.pod_ip, "namespace": i.metadata.namespace}
        return render(request, "k8s-pod-list.html", {"data": data})

class K8sPodWebssh(View):

    def get(self, request):
        name = self.request.GET.get("name")
        namespace = self.request.GET.get("namespace")
        return render(request, "k8s-pod-webssh.html", {"name": name, "namespace": namespace})