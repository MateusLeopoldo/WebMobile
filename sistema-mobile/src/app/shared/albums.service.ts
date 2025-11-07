import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

export interface AlbumItem {
  id: number;
  titulo: string;
  artista: string;
  ano_lancamento: number;
  preco: number;
  preco_formatado: string | null;
  foto_url: string | null;
}

export interface AlbumListResponse {
  count: number;
  results: AlbumItem[];
}

@Injectable({ providedIn: 'root' })
export class AlbumsService {
  private base = environment.apiBase;

  constructor(private http: HttpClient) {}

  listar(q?: string): Observable<AlbumListResponse> {
    let params = new HttpParams();
    if (q) {
      params = params.set('q', q);
    }
    return this.http.get<AlbumListResponse>(`${this.base}/api/albums/`, { params });
  }
}