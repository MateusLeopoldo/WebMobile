import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../shared/auth.service';
import { Credenciais } from './usuario.model';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent, IonItem, IonInput, IonButton, IonText, IonSpinner, IonIcon
} from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { musicalNotes } from 'ionicons/icons';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: true,
  imports: [
    CommonModule, FormsModule,
    IonContent, IonItem, IonInput, IonButton, IonText, IonSpinner, IonIcon
  ],
})
export class LoginPage {
  form: Credenciais = { username: '', password: '' };
  loading = false;
  error: string | null = null;

  constructor(private auth: AuthService, private router: Router) {
    addIcons({ musicalNotes });
  }

  submit() {
    this.loading = true;
    this.error = null;
    this.auth.login(this.form).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigateByUrl('/home', { replaceUrl: true });
      },
      error: (err) => {
        this.loading = false;
        this.error = err?.error?.detail || 'Falha no login';
      }
    });
  }
}