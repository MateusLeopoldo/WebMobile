import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AlbumsService, AlbumItem } from '../shared/albums.service';
import { AuthService } from '../shared/auth.service';
import {
  IonHeader, IonToolbar, IonTitle, IonContent, IonButtons, IonButton,
  IonSearchbar, IonSpinner, IonText, IonIcon
} from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { logOutOutline, discOutline } from 'ionicons/icons';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    IonHeader, IonToolbar, IonTitle, IonContent, IonButtons, IonButton,
    IonSearchbar, IonSpinner, IonText, IonIcon
  ],
})
export class HomePage {
  loading = true;
  error: string | null = null;
  albums: AlbumItem[] = [];

  constructor(
    private albumsSvc: AlbumsService,
    private auth: AuthService,
    private router: Router
  ) {
    addIcons({ logOutOutline, discOutline });
  }

  ionViewWillEnter() {
    this.load();
  }

  load(q?: string | null) {
    this.loading = true;
    this.error = null;
    this.albumsSvc.listar(q || undefined).subscribe({
      next: (res) => {
        this.albums = res.results;
        this.loading = false;
      },
      error: (err) => {
        this.error = err?.error?.detail || 'Erro ao carregar álbuns';
        this.loading = false;
      }
    });
  }

  logout() {
    this.auth.logout();
    this.router.navigateByUrl('/', { replaceUrl: true });
  }
}
