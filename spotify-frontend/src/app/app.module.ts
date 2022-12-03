import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {TextFieldModule} from '@angular/cdk/text-field';
import { MatFormFieldModule } from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input'
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { InputComponent } from './input/input.component';
import { MatButtonModule } from '@angular/material/button';
import { HttpClientModule } from '@angular/common/http';
import { DisplayComponent } from './display/display.component';
import {MatTableModule} from '@angular/material/table';
import { AudioComponent } from './audio/audio.component';
import { ToastrModule } from 'ngx-toastr';
import {MatGridListModule} from '@angular/material/grid-list'; 
import {MatDialogModule} from '@angular/material/dialog';

@NgModule({
  declarations: [
    AppComponent,
    InputComponent,
    DisplayComponent,
    AudioComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatFormFieldModule,
    MatInputModule,
    BrowserAnimationsModule,
    TextFieldModule,
    MatButtonModule,
    MatDialogModule,
    HttpClientModule,
    MatTableModule,
    MatGridListModule,
    ToastrModule.forRoot({
      positionClass: 'toast-top-full-width'
    }),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
