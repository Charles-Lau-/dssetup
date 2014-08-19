#coding=utf-8
from django.conf.urls import patterns, url
from dssetup.action import formAction
 

urlpatterns =  patterns('',
       #show_xxx 是用来显示列表的域名。比如 我想要进入显示 已申请表单列表这样一个页面  那么 就是提交  show_applied_form的请求                                   
       url(r"^show_applied_form$",formAction.showAppliedForm,name="show_applied_form"),
       url(r"show_unverified_form$",formAction.showUnverifiedForm,name="show_unverified_form"),
       url(r"show_unchecked_form$",formAction.showUncheckedForm,name="show_unchecked_form"),
       url(r"show_unimplemented_form",formAction.showUnimplementedForm,name="show_unimplemented_form"),                
       
       #apply_form/ 这个事 用来处理一切和申请表单相关的请求的，因为申请表单 分为几个部件 很复杂
       #create_main_form 是 显示表单的主要部分
       #create_mapping_fomr 是显示表单的映射部分
       #store_domainName  是 填写了域名 并点击保存后的请求对应的url
       #create_mapping_part 是相当于中转站   介于申请表单主要内容 和申请表单映射内容中间  进行 这两个部分内容的显示  
       url( r"^apply_form/create_main_form",formAction.createDomainForm,name="create_main_form"),
       url(r"^apply_form/create_mapping_form/(?P<domainName>\S*)$",formAction.createMappingForm,name="create_mapping_form"),
       url(r"^apply_form/store_domainName$",formAction.storeDomainName,name="store_domainName"),
       url(r"^apply_form/create_mapping_part$",formAction.createMappingPart,name="create_mapping_part"),
       url(r"^apply_form/delete_mapping_form/(?P<domainName>\S+)/(?P<Id>\d+)$",formAction.deleteMappingForm,name="delete_mapping_form"),
       url(r"^apply_form/delete_domain_form/(?P<domainName>\S+)$",formAction.deleteDomainForm,name="delete_domain_form"),  
       url(r"^apply_form/submit$",formAction.addFormIntoDatabase,name="add_form"),                 
       
       #check_form  是  当你在表单显示列表 点击 某个表单进行查看详细信息时候使用的
       #change_form 是当你进行了某个操作 比如审核 或者关闭的时候使用的
       #edit_form 就很容易理解了 编辑表单使用
       #cancel_edit 是放弃编辑  form_history 是去查看表单的 状态流转
       url(r"^check_form/(?P<Id>\d+)/(?P<role>\S*)$",formAction.checkForm,name="check_form"),
       url(r"^change_form/$",formAction.changeForm,name="change_form_status"),
       url(r"^edit_form/(?P<Id>\d+)/(?P<step>\d*)$",formAction.editForm,name="edit_form"),
       url(r"^cancel_edit$",formAction.cancelEdit,name="cancel_edit"),
       url(r"^form_history/(?P<Id>\d+)$",formAction.showFormHistory,name="show_form_history"),
            )