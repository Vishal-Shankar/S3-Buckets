from django.shortcuts import render
import boto3
from django.contrib import messages

# Create your views here.
def Buck(request):
    
    if request.method == 'POST':
        aid=request.POST.get('aid')
        sak=request.POST.get('sak')
        n=request.POST.get('name')
        fn=request.POST.get('fname')
        bn=request.POST.get('bname')
        cr=request.POST.get('crb')
        dl=request.POST.get('del')
        crf=request.POST.get('crf')
        lb=request.POST.get('lb')
        crfo=request.POST.get('crfo')
        lf=request.POST.get('lf')
        uf=request.POST.get('uf')
        sbn=request.POST.get('sbname')
        sfn=request.POST.get('sfname')
        dbn=request.POST.get('dbname')
        dfn=request.POST.get('dfname')
        cf=request.POST.get('cf')
        mf=request.POST.get('mf')
        df=request.POST.get('df')
        dfo=request.POST.get('dfo')
        try:
            if aid and sak:
                s3=boto3.resource(
                                    service_name='s3',
                                    region_name='us-east-1',
                                    aws_access_key_id = aid,
                                    aws_secret_access_key = sak,
                                    ) 
                if cr:
                    if n:
                        if n not in [i.name for i in s3.buckets.all()]:
                            try:
                                s3.create_bucket(Bucket=n)
                                messages.success(request,f'{n} created successfully click in list buckets to verify')
                                return render(request,'home.html')
                            except:
                                messages.error(request,'Bucket aldready exist please try a diffrent name')
                                return render(request,'home.html')
                        else:
                            messages.error(request,'Bucket aldready exist please try a diffrent name')
                            return render(request,'home.html')
                    else:
                        messages.error(request,'Please Enter Bucket name')
                        return render(request,'home.html')            
                if dl:
                    if n:
                        if n in [i.name for i in s3.buckets.all()]:
                            bck=s3.Bucket(n)
                            bck.objects.all().delete()
                            bck.delete()
                            messages.success(request,f'{n} Deleted successfully click on List Buckets to verify')
                            return render(request,'home.html')
                        else:
                            messages.error(request,'Bucket does not exist please try a valid name')
                            return render(request,'home.html')
                    else:
                        messages.error(request,'Please Enter Bucket name')
                        return render(request,'home.html')
                if lb:
                    return render(request,'cmplt.html',{'lbs':[i for i in s3.buckets.all()]})
                if crf:
                    if bn and fn:
                        if bn in [i.name for i in s3.buckets.all()]:
                            s3.Bucket(bn).put_object(Key=fn)
                            messages.success(request,f'{fn} created successfully click on List Files/Folder to verify')
                        else:
                            messages.error(request,'Bucket doesnt exist please enter a diffrent name')
                            return render(request,'home.html')
                    else:
                        messages.error(request,'Please Enter all the * fields')
                        return render(request,'home.html')
                if crfo:
                    if bn and fn:
                        if bn in [i.name for i in s3.buckets.all()]:
                            fn+='/'
                            s3.Bucket(bn).put_object(Key=fn)
                            messages.success(request,f'{fn} created successfully click on List Files/Folder to verify')
                        else:
                            messages.error(request,'Bucket doesnt exist please enter a diffrent name')
                            return render(request,'home.html')
                    else:
                        messages.error(request,'Please Enter all the * fields')
                        return render(request,'home.html')
                if lf:
                    myb=s3.Bucket(bn)
                    if bn:
                        data=[i.name for i in s3.buckets.all()]
                        if bn in data:
                            return render(request,'cmplt.html',{'lfs':[i.key for i in myb.objects.all()]})
                        else:
                            messages.error(request,'Bucket does not exist please try a valid name')
                            return render(request,'home.html')          
                    else:
                        messages.error(request,'Please Enter Bucket Name for listing the files and folders')
                if uf:
                    if bn and fn:
                        try:
                            with open(fn,'rb') as f:
                                s3.Bucket(bn).put_object(Key=[fn.split('/')][-1][-1],Body=f)
                                fns=[fn.split('/')][-1][-1]
                                messages.success(request,f'{fns} Uploaded successfully click on List Files to verify')
                        except:
                            messages.error(request,'Please Enter a valid file path')
                    else:
                        messages.error(request,'Please Enter all the * fields')
                        return render(request,'home.html')
                if cf:
                    if sbn and sfn and dbn and dfn:
                        nbm=[i.name for i in s3.buckets.all()]
                        if sbn in nbm and dbn in nbm:
                            mys=s3.Bucket(sbn)
                            myd=s3.Bucket(dbn)
                            nsfm=[i.key for i in mys.objects.all()]
                            ndfm=[i.key for i in myd.objects.all()]
                            if sfn in nsfm and dfn in ndfm:
                                cs={
                                    'Bucket':sbn,
                                    'Key':sfn
                                }
                                buck = s3.Bucket(dbn)
                                buck.copy(cs,dfn)
                                messages.success(request,f'Copied content of {sbn}/{sfn} to {dbn}/{dfn} successfully')
                            else:
                                messages.error(request,'invalid source or destination file name please enter valid names')
                                return render(request,'home.html')
                        else:
                            messages.error(request,'invalid source or destination bucket name please enter valid names')
                            return render(request,'home.html')
                            
                    else:
                        messages.error(request,'Please Enter all the $ fields')
                        return render(request,'home.html')        
                if mf:
                    if sbn and sfn and dbn:
                        nbm=[i.name for i in s3.buckets.all()]
                        if sbn in nbm and dbn in nbm:
                            myd=s3.Bucket(sbn)
                            nsfd=[i.key for i in myd.objects.all()]
                            if sfn in nsfd:
                                s3.Bucket(dbn).put_object(Key=sfn)
                                css={
                                    'Bucket':sbn,
                                    'Key':sfn
                                }
                                bck = s3.Bucket(dbn)
                                bck.copy(css,sfn)
                                s3.Object(sbn,sfn).delete()
                                messages.success(request,f'Moved {sfn} from {sbn} to {dbn} successfully')
                            else:
                                messages.error(request,'invalid source file name please enter valid names')
                                return render(request,'home.html')
                        else:
                            messages.error(request,'invalid source or destination bucket name please enter valid names')
                            return render(request,'home.html')
                    else:
                        messages.error(request,'Please Enter all the # fields')
                        return render(request,'home.html')   
                if df:
                    if bn and fn:
                        mfb=s3.Bucket(bn)
                        if bn in [i.name for i in s3.buckets.all()]:
                            if fn in [i.key for i in mfb.objects.all()]:
                                s3.Object(bn,fn).delete()
                                messages.success(request,f'{fn} deleted  successfully click on List Files/Folder to verify')
                            else:
                                messages.error(request,'File does not exist please try a valid name')
                                return render(request,'home.html')          
                        else:
                            messages.error(request,'Bucket does not exist please try a valid name')
                            return render(request,'home.html')          
                    else:
                        messages.error(request,'Please Enter all the * fields')
                        return render(request,'home.html') 
                if dfo:
                    if bn and fn:
                        mfb=s3.Bucket(bn)
                        if bn in [i.name for i in s3.buckets.all()]:
                            fn+='/'
                            if fn in [i.key for i in mfb.objects.all()]:
                                s3.Object(bn,fn).delete()
                                messages.success(request,f'{fn} deleted  successfully click on List Files/Folder to verify')
                            else:
                                messages.error(request,'File does not exist please try a valid name')
                                return render(request,'home.html')          
                        else:
                            messages.error(request,'Bucket does not exist please try a valid name')
                            return render(request,'home.html')          
                    else:
                        messages.error(request,'Please Enter all the * fields')
                        return render(request,'home.html') 
            else:
                messages.error(request,'Please Enter Access Key Id and Secret Access Key')
                return render(request,'home.html')
        except:
            messages.error(request,'Invalid Access Key Id and Secret Access Key')
            return render(request,'home.html')
    else:
        return render(request,'home.html')
    return render(request,'home.html')

