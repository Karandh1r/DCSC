import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor(private http:HttpClient) {
    }
    getSongdata(search:any){
      return this.http.get('http://localhost/spotify/artist/'+ search);
    } 
}
