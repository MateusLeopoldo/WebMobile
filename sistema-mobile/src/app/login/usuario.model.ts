export class Usuario
{
  public id: number;
  public nome: string;
  public email: string;
  public token: string;

  constructor() { 
    this.id = 0;
    this.nome = '';
    this.email = '';
    this.token = '';
  }
}

export interface Credenciais {
  username: string;
  password: string;
}

export interface JwtTokens {
  access: string;
  refresh: string;
}