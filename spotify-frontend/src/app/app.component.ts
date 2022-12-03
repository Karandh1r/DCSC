import { Component,OnInit } from '@angular/core';
import {ApiService} from  './api.service';
import {AudioComponent} from './audio/audio.component'
import {MatDialog, MatDialogRef} from '@angular/material/dialog';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'spotify-frontend';
  all_records: Array<any>
  constructor(private api: ApiService,public dialog: MatDialog) {  
 }
 openDialog(): void {
  const dialogRef = this.dialog.open(AudioComponent, {
    width: '400px',
    height : '250px'
  });
  dialogRef.afterClosed().subscribe(result => {
    console.log('The dialog was closed');
  }); 
}
  handleSpotifyDbClick(eventData: { searchquery: string }){
      this.api.getSongdata(eventData.searchquery).subscribe((data : any)=>{
      this.all_records = data.tracks
      console.log(this.all_records)
   });
  }
  
}
