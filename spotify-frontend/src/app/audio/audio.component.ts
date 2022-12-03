import { Component,ViewChild,ElementRef } from '@angular/core';
import {  HttpEvent, HttpEventType } from '@angular/common/http';
import {ApiService} from '../api.service'
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-audio',
  templateUrl: './audio.component.html',
  styleUrls: ['./audio.component.css']
})
export class AudioComponent  {
  file : File | null = null;;
  progress: number = 0;
  @ViewChild('myInput',{static: true}) myInputVariable: ElementRef;

  constructor(private apiService: ApiService,private toastrService: ToastrService) { }
  onFileChange(event : any) {
    if (event.target.files.length > 0) {
      this.file = event.target.files[0];
    }
  }
  upload(){
    this.apiService.fileUpload(this.file).subscribe(
      (event:  HttpEvent<any>) => {
          //this.shortLink = event.link;
          this.resetFile();
          switch(event.type){
              case HttpEventType.UploadProgress:
                const total: number | any = event.total;
                this.progress = Math.round(event.loaded / (total * 100));
                break;
              case HttpEventType.ResponseHeader:
                if(event.status == 200){
                  this.toastrService.success("File was uploaded successfully");         
                }
                if(event.status == 500){
                  this.toastrService.error("Error while uploading file");
                }
          }

      });
  }
  fileIsUploaded()
  {
    let result = false;
    if(this.file && this.file != null )
    {
      result = true;
    }
    return result;
  }

  resetFile()
  {
    this.myInputVariable.nativeElement.value = "";
    this.file = null
    this.progress = 0;
  }  
}


