from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging


logger = logging.getLogger(__name__)


class EmailService:
    """Serviço para envio de emails"""
    
    def __init__(self):
        """Inicializa o serviço de email com URL do frontend"""
        self.frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')

    @staticmethod
    def _get_user_name(user):
        """
        Retorna o nome do usuário de forma segura
        """
        # Tentar pegar nome do perfil, username ou email
        if hasattr(user, 'name') and user.name:
            return user.name
        elif hasattr(user, 'username') and user.username:
            return user.username
        elif user.email:
            return user.email.split('@')[0]
        return 'Usuário'

    @staticmethod
    def send_notification_email(user, notification):
        """
        Envia email de notificação para o usuário
        """
        try:
            subject = f'Metflix - {notification.title}'
            user_name = EmailService._get_user_name(user)
            
            # HTML Email
            html_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }}
                    .email-container {{
                        max-width: 600px;
                        margin: 20px auto;
                        background-color: #ffffff;
                        border-radius: 8px;
                        overflow: hidden;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }}
                    .email-header {{
                        background-color: #e50914;
                        color: #ffffff;
                        padding: 20px;
                        text-align: center;
                    }}
                    .email-body {{
                        padding: 30px;
                        color: #333333;
                    }}
                    .email-footer {{
                        background-color: #f4f4f4;
                        padding: 20px;
                        text-align: center;
                        font-size: 12px;
                        color: #666666;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">
                        <h1>METFLIX</h1>
                    </div>
                    <div class="email-body">
                        <h2>{notification.title}</h2>
                        <p>{notification.message}</p>
                        <p style="margin-top: 20px;">
                            <strong>Data:</strong> {notification.created_at.strftime('%d/%m/%Y às %H:%M')}
                        </p>
                    </div>
                    <div class="email-footer">
                        <p>© 2024 Metflix. Todos os direitos reservados.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Plain text version
            plain_message = strip_tags(html_message)
            
            # Send email
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            
            email.attach_alternative(html_message, "text/html")
            email.send()
            
            logger.info(f'✅ Email enviado para {user.email}')
            return True
            
        except Exception as e:
            logger.error(f'❌ Erro ao enviar email: {str(e)}', exc_info=True)
            return False

    @staticmethod
    def send_favorite_added_email(user, media_title, media_type='filme', media_id=None):
        """
        Envia email quando um filme/série é adicionado à lista
        Args:
            user: Usuário que adicionou
            media_title: Título do filme/série
            media_type: 'filme' ou 'série'
            media_id: ID do filme/série (opcional)
        """
        try:
            subject = f'Metflix - {media_title} foi adicionado à sua lista'
            user_name = EmailService._get_user_name(user)
            
            # Emoji baseado no tipo
            emoji = "🎬" if media_type.lower() == 'filme' else "📺"
            
            # HTML Email
            html_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: 'Helvetica Neue', Arial, sans-serif;
                        background-color: #141414;
                        margin: 0;
                        padding: 0;
                    }}
                    .email-container {{
                        max-width: 600px;
                        margin: 20px auto;
                        background-color: #ffffff;
                        border-radius: 8px;
                        overflow: hidden;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                    }}
                    .email-header {{
                        background: linear-gradient(135deg, #e50914 0%, #b20710 100%);
                        color: #ffffff;
                        padding: 30px 20px;
                        text-align: center;
                    }}
                    .email-header h1 {{
                        margin: 0;
                        font-size: 32px;
                        font-weight: 700;
                        letter-spacing: 2px;
                    }}
                    .email-body {{
                        padding: 40px 30px;
                        color: #333333;
                        background-color: #ffffff;
                    }}
                    .media-info {{
                        background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
                        padding: 25px;
                        border-radius: 8px;
                        margin: 20px 0;
                        border-left: 4px solid #e50914;
                    }}
                    .media-title {{
                        font-size: 24px;
                        font-weight: 700;
                        color: #e50914;
                        margin-bottom: 10px;
                    }}
                    .media-type {{
                        display: inline-block;
                        background-color: #e50914;
                        color: #ffffff;
                        padding: 6px 12px;
                        border-radius: 4px;
                        font-size: 12px;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                    }}
                    .button {{
                        display: inline-block;
                        padding: 14px 32px;
                        background: linear-gradient(135deg, #e50914 0%, #b20710 100%);
                        color: #ffffff;
                        text-decoration: none;
                        border-radius: 6px;
                        margin-top: 25px;
                        font-weight: 600;
                        font-size: 16px;
                        box-shadow: 0 4px 8px rgba(229, 9, 20, 0.3);
                    }}
                    .email-footer {{
                        background-color: #f9f9f9;
                        padding: 25px;
                        text-align: center;
                        font-size: 13px;
                        color: #666666;
                        border-top: 1px solid #e0e0e0;
                    }}
                    .emoji {{
                        font-size: 48px;
                        margin-bottom: 15px;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">
                        <h1>METFLIX</h1>
                    </div>
                    <div class="email-body">
                        <div style="text-align: center;">
                            <div class="emoji">{emoji}</div>
                            <h2 style="color: #333; margin-bottom: 10px;">Adicionado à Minha Lista!</h2>
                            <p style="color: #666; font-size: 16px;">Olá, {user_name}! 👋</p>
                        </div>
                        
                        <div class="media-info">
                            <div class="media-type">{media_type.upper()}</div>
                            <div class="media-title">{media_title}</div>
                            <p style="color: #666; margin: 10px 0 0 0;">
                                Foi adicionado à sua lista de favoritos com sucesso!
                            </p>
                        </div>
                        
                        <p style="margin-top: 25px; color: #666; line-height: 1.6;">
                            Você pode assistir agora ou deixar para mais tarde. 
                            Sua lista está sempre disponível no menu <strong>"Minha Lista"</strong>.
                        </p>
                        
                        <div style="text-align: center;">
                            <a href="http://localhost:5173/minha-lista" class="button">
                                Ver Minha Lista
                            </a>
                        </div>
                    </div>
                    <div class="email-footer">
                        <p style="margin: 0 0 10px 0;">
                            <strong>Metflix</strong> - Seu streaming favorito
                        </p>
                        <p style="margin: 0; font-size: 12px; color: #999;">
                            © 2024 Metflix. Todos os direitos reservados.
                        </p>
                        <p style="margin: 10px 0 0 0; font-size: 11px; color: #999;">
                            Este é um email automático, por favor não responda.
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Plain text version
            plain_message = f"""
            METFLIX - {media_title} foi adicionado à sua lista
            
            Olá, {user_name}!
            
            {emoji} {media_type.upper()}: {media_title}
            
            Foi adicionado à sua lista de favoritos com sucesso!
            
            Você pode assistir agora ou deixar para mais tarde.
            Sua lista está sempre disponível no menu "Minha Lista".
            
            Ver Minha Lista: http://localhost:5173/minha-lista
            
            ---
            Metflix - Seu streaming favorito
            © 2024 Metflix. Todos os direitos reservados.
            """
            
            # Send email
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            
            email.attach_alternative(html_message, "text/html")
            email.send()
            
            logger.info(f'✅ Email de favorito enviado para {user.email}: {media_title}')
            return True
            
        except Exception as e:
            logger.error(f'❌ Erro ao enviar email de favorito: {str(e)}', exc_info=True)
            return False

    def send_welcome_email(self, user):
        """
        Envia email de boas-vindas para novo usuário.
        
        Args:
            user: Objeto User do Django
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        try:
            # Dados do usuário
            user_name = self._get_user_name(user)
            user_email = user.email
            
            # Assunto do email
            subject = f"🎬 Bem-vindo ao Metflix, {user_name}!"
            
            # Corpo do email em HTML
            html_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        background-color: #141414;
                        color: #ffffff;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #000000;
                    }}
                    .header {{
                        background: linear-gradient(to right, #e50914, #b20710);
                        padding: 40px 20px;
                        text-align: center;
                    }}
                    .logo {{
                        font-size: 48px;
                        font-weight: 700;
                        color: #ffffff;
                        letter-spacing: 3px;
                        margin: 0;
                    }}
                    .content {{
                        padding: 40px 30px;
                        background-color: #141414;
                    }}
                    .welcome-title {{
                        font-size: 32px;
                        font-weight: 700;
                        color: #ffffff;
                        margin: 0 0 20px 0;
                        text-align: center;
                    }}
                    .welcome-text {{
                        font-size: 18px;
                        color: #b3b3b3;
                        line-height: 1.6;
                        margin: 20px 0;
                    }}
                    .highlight {{
                        color: #e50914;
                        font-weight: 600;
                    }}
                    .features {{
                        background-color: #1a1a1a;
                        border-radius: 8px;
                        padding: 30px;
                        margin: 30px 0;
                    }}
                    .feature-item {{
                        margin: 20px 0;
                        display: flex;
                        align-items: flex-start;
                    }}
                    .feature-icon {{
                        font-size: 24px;
                        margin-right: 15px;
                        flex-shrink: 0;
                    }}
                    .feature-text {{
                        font-size: 16px;
                        color: #e5e5e5;
                        line-height: 1.5;
                    }}
                    .cta-button {{
                        display: inline-block;
                        background-color: #e50914;
                        color: #ffffff;
                        text-decoration: none;
                        padding: 16px 40px;
                        border-radius: 4px;
                        font-size: 18px;
                        font-weight: 600;
                        margin: 30px 0;
                        text-align: center;
                    }}
                    .footer {{
                        background-color: #000000;
                        padding: 30px 20px;
                        text-align: center;
                        color: #808080;
                        font-size: 14px;
                    }}
                    .footer a {{
                        color: #e50914;
                        text-decoration: none;
                    }}
                    .divider {{
                        height: 1px;
                        background: linear-gradient(to right, transparent, #333, transparent);
                        margin: 30px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <!-- Header -->
                    <div class="header">
                        <h1 class="logo">METFLIX</h1>
                    </div>
                    
                    <!-- Content -->
                    <div class="content">
                        <h2 class="welcome-title">🎉 Bem-vindo ao Metflix!</h2>
                        
                        <p class="welcome-text">
                            Olá <span class="highlight">{user_name}</span>! 👋
                        </p>
                        
                        <p class="welcome-text">
                            Sua conta foi criada com sucesso! Estamos muito felizes em ter você conosco.
                        </p>
                        
                        <p class="welcome-text">
                            Agora você pode desfrutar de:
                        </p>
                        
                        <!-- Features -->
                        <div class="features">
                            <div class="feature-item">
                                <div class="feature-icon">🎬</div>
                                <div class="feature-text">
                                    <strong>Acesso ilimitado</strong><br>
                                    Milhares de filmes e séries à sua disposição
                                </div>
                            </div>
                            
                            <div class="feature-item">
                                <div class="feature-icon">❤️</div>
                                <div class="feature-text">
                                    <strong>Lista de Favoritos</strong><br>
                                    Salve seus conteúdos preferidos e receba notificações
                                </div>
                            </div>
                            
                            <div class="feature-item">
                                <div class="feature-icon">👤</div>
                                <div class="feature-text">
                                    <strong>Múltiplos Perfis</strong><br>
                                    Crie perfis personalizados para toda família
                                </div>
                            </div>
                            
                            <div class="feature-item">
                                <div class="feature-icon">🔔</div>
                                <div class="feature-text">
                                    <strong>Recomendações</strong><br>
                                    Sugestões personalizadas baseadas no seu gosto
                                </div>
                            </div>
                        </div>
                        
                        <div style="text-align: center;">
                            <a href="{self.frontend_url}" class="cta-button">
                                🚀 Começar a Assistir
                            </a>
                        </div>
                        
                        <div class="divider"></div>
                        
                        <p class="welcome-text" style="font-size: 16px;">
                            <strong>📧 Seu email de acesso:</strong><br>
                            {user_email}
                        </p>
                        
                        <p class="welcome-text" style="font-size: 14px; color: #808080;">
                            💡 <strong>Dica:</strong> Crie seu primeiro perfil e comece a adicionar seus filmes favoritos à sua lista!
                        </p>
                    </div>
                    
                    <!-- Footer -->
                    <div class="footer">
                        <p>© 2024 Metflix, Inc. Todos os direitos reservados.</p>
                        <p>
                            <a href="{self.frontend_url}/help">Central de Ajuda</a> | 
                            <a href="{self.frontend_url}/terms">Termos de Uso</a> | 
                            <a href="{self.frontend_url}/privacy">Privacidade</a>
                        </p>
                        <p style="margin-top: 20px; font-size: 12px;">
                            Você recebeu este email porque criou uma conta no Metflix.
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Plain text version
            plain_message = f"""
            METFLIX - Bem-vindo ao Metflix!
            
            Olá, {user_name}! 👋
            
            Sua conta foi criada com sucesso! Estamos muito felizes em ter você conosco.
            
            Agora você pode desfrutar de:
            
            🎬 Acesso ilimitado
            Milhares de filmes e séries à sua disposição
            
            ❤️ Lista de Favoritos
            Salve seus conteúdos preferidos e receba notificações
            
            👤 Múltiplos Perfis
            Crie perfis personalizados para toda família
            
            🔔 Recomendações
            Sugestões personalizadas baseadas no seu gosto
            
            🚀 Começar a Assistir: {self.frontend_url}
            
            📧 Seu email de acesso: {user_email}
            
            💡 Dica: Crie seu primeiro perfil e comece a adicionar seus filmes favoritos à sua lista!
            
            ---
            © 2024 Metflix, Inc. Todos os direitos reservados.
            
            Central de Ajuda: {self.frontend_url}/help
            Termos de Uso: {self.frontend_url}/terms
            Privacidade: {self.frontend_url}/privacy
            
            Você recebeu este email porque criou uma conta no Metflix.
            """
            
            # Send email
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user_email]
            )
            
            email.attach_alternative(html_message, "text/html")
            email.send()
            
            logger.info(f'✅ Email de boas-vindas enviado para {user_email}')
            return True
            
        except Exception as e:
            logger.error(f'❌ Erro ao enviar email de boas-vindas: {str(e)}', exc_info=True)
            return False

    def send_account_deleted_email(self, user_email, user_name):
        """
        Envia email de confirmação de exclusão de conta.
        
        Args:
            user_email: Email do usuário
            user_name: Nome do usuário
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        try:
            subject = "Metflix - Conta Excluída"
            
            # Corpo do email em HTML
            html_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        background-color: #141414;
                        color: #ffffff;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #000000;
                    }}
                    .header {{
                        background: linear-gradient(to right, #555, #333);
                        padding: 40px 20px;
                        text-align: center;
                    }}
                    .logo {{
                        font-size: 48px;
                        font-weight: 700;
                        color: #ffffff;
                        letter-spacing: 3px;
                        margin: 0;
                    }}
                    .content {{
                        padding: 40px 30px;
                        background-color: #141414;
                    }}
                    .title {{
                        font-size: 28px;
                        font-weight: 700;
                        color: #ffffff;
                        margin: 0 0 20px 0;
                        text-align: center;
                    }}
                    .text {{
                        font-size: 16px;
                        color: #b3b3b3;
                        line-height: 1.6;
                        margin: 20px 0;
                    }}
                    .highlight {{
                        color: #ffffff;
                        font-weight: 600;
                    }}
                    .info-box {{
                        background-color: #1a1a1a;
                        border-left: 4px solid #666;
                        border-radius: 4px;
                        padding: 20px;
                        margin: 30px 0;
                    }}
                    .footer {{
                        background-color: #000000;
                        padding: 30px 20px;
                        text-align: center;
                        color: #808080;
                        font-size: 14px;
                    }}
                    .divider {{
                        height: 1px;
                        background: linear-gradient(to right, transparent, #333, transparent);
                        margin: 30px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <!-- Header -->
                    <div class="header">
                        <h1 class="logo">METFLIX</h1>
                    </div>
                    
                    <!-- Content -->
                    <div class="content">
                        <h2 class="title">Conta Excluída</h2>
                        
                        <p class="text">
                            Olá <span class="highlight">{user_name}</span>,
                        </p>
                        
                        <p class="text">
                            Sua conta no Metflix foi excluída permanentemente conforme solicitado.
                        </p>
                        
                        <div class="info-box">
                            <p class="text" style="margin: 0 0 10px 0;">
                                <strong>⚠️ O que foi excluído:</strong>
                            </p>
                            <ul style="color: #b3b3b3; margin: 0; padding-left: 20px;">
                                <li>Seus dados pessoais</li>
                                <li>Todos os perfis criados</li>
                                <li>Sua lista de favoritos</li>
                                <li>Histórico de atividades</li>
                                <li>Preferências e configurações</li>
                            </ul>
                        </div>
                        
                        <p class="text">
                            Sentimos muito em vê-lo partir. Se você mudou de ideia, pode criar uma nova conta a qualquer momento.
                        </p>
                        
                        <div class="divider"></div>
                        
                        <p class="text" style="text-align: center;">
                            <strong>Email excluído:</strong> {user_email}
                        </p>
                        
                        <p class="text" style="font-size: 14px; color: #808080; text-align: center;">
                            Obrigado por ter feito parte da nossa comunidade! 💙
                        </p>
                    </div>
                    
                    <!-- Footer -->
                    <div class="footer">
                        <p>© 2024 Metflix, Inc. Todos os direitos reservados.</p>
                        <p style="margin-top: 20px; font-size: 12px;">
                            Se você não solicitou esta exclusão, entre em contato conosco imediatamente.
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Plain text version
            plain_message = f"""
            METFLIX - Conta Excluída
            
            Olá {user_name},
            
            Sua conta no Metflix foi excluída permanentemente conforme solicitado.
            
            ⚠️ O que foi excluído:
            - Seus dados pessoais
            - Todos os perfis criados
            - Sua lista de favoritos
            - Histórico de atividades
            - Preferências e configurações
            
            Sentimos muito em vê-lo partir. Se você mudou de ideia, pode criar uma nova conta a qualquer momento.
            
            Email excluído: {user_email}
            
            Obrigado por ter feito parte da nossa comunidade! 💙
            
            ---
            © 2024 Metflix, Inc. Todos os direitos reservados.
            
            Se você não solicitou esta exclusão, entre em contato conosco imediatamente.
            """
            
            # Send email
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user_email]
            )
            
            email.attach_alternative(html_message, "text/html")
            email.send()
            
            logger.info(f'✅ Email de exclusão de conta enviado para {user_email}')
            return True
            
        except Exception as e:
            logger.error(f'❌ Erro ao enviar email de exclusão: {str(e)}', exc_info=True)
            return False
