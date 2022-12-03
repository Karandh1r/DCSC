import { Injectable } from '@angular/core';
import { HttpClient , HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';



@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor(private http:HttpClient) {
    }
    getSongdata(search:any){
      return this.http.get('http://localhost/spotify/artist/'+ search);
    } 
    fileUpload(file : any):Observable<any> {
      let headers = new HttpHeaders({
        'FileName': file.name
      });
      //return this.http.post('http://localhost/spotify/voice',formData)
      return this.http.post('http://localhost/spotify/voice',file,{
        headers,
        reportProgress : true,
        observe: 'events'
  
      })
    }
}
