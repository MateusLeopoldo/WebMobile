import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable, tap } from 'rxjs';
import { Credenciais } from '../login/usuario.model';

interface JwtTokens { access: string; refresh?: string; }

@Injectable({ providedIn: 'root' })
export class AuthService {
  private base = environment.apiBase;
  constructor(private http: HttpClient) {}

  login(body: Credenciais): Observable<JwtTokens> {
    return this.http.post<JwtTokens>(`${this.base}/api/auth/login/`, body).pipe(
      tap(tokens => {
        if (tokens.access) localStorage.setItem('access_token', tokens.access);
        if ((tokens as any).refresh) localStorage.setItem('refresh_token', (tokens as any).refresh);
      })
    );
  }
}