from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.models import Profile
from core.serializers.profile import ProfileSerializer
import logging

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profiles_list(request):
    """
    GET: Listar perfis do usuário logado
    POST: Criar novo perfil
    """
    if request.method == 'GET':
        try:
            profiles = Profile.objects.filter(user=request.user)
            serializer = ProfileSerializer(profiles, many=True)
            logger.info(f"✅ Listando {profiles.count()} perfis para {request.user.email}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"❌ Erro ao listar perfis: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Erro ao listar perfis'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'POST':
        try:
            serializer = ProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                logger.info(f"✅ Perfil criado: {serializer.data['name']} para {request.user.email}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            logger.warning(f"⚠️ Erro de validação: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"❌ Erro ao criar perfil: {str(e)}", exc_info=True)
            return Response(
                {'error': f'Erro ao criar perfil: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile_detail(request, pk):
    """
    GET: Buscar perfil específico
    PUT: Atualizar perfil
    DELETE: Deletar perfil
    """
    try:
        # ✅ Garantir que o perfil pertence ao usuário
        profile = Profile.objects.get(pk=pk, user=request.user)
    except Profile.DoesNotExist:
        logger.warning(f"⚠️ Perfil {pk} não encontrado para usuário {request.user.email}")
        return Response(
            {'error': 'Perfil não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"❌ Erro ao buscar perfil: {str(e)}", exc_info=True)
        return Response(
            {'error': f'Erro ao buscar perfil: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if request.method == 'GET':
        try:
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"❌ Erro ao serializar perfil: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Erro ao buscar perfil'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'PUT':
        try:
            # ✅ partial=True permite atualizar apenas alguns campos
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                logger.info(f"✅ Perfil atualizado: {profile.name}")
                return Response(serializer.data)
            
            logger.warning(f"⚠️ Erro de validação ao atualizar: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar perfil: {str(e)}", exc_info=True)
            return Response(
                {'error': f'Erro ao atualizar perfil: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'DELETE':
        try:
            # ✅ Verificar se não é o último perfil
            user_profiles_count = Profile.objects.filter(user=request.user).count()
            
            if user_profiles_count <= 1:
                logger.warning(f"⚠️ Tentativa de deletar último perfil do usuário {request.user.email}")
                return Response(
                    {'error': 'Você precisa ter pelo menos um perfil'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            profile_name = profile.name
            profile.delete()
            logger.info(f"✅ Perfil deletado: {profile_name}")
            
            return Response(
                {'message': f'Perfil "{profile_name}" deletado com sucesso'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao deletar perfil: {str(e)}", exc_info=True)
            return Response(
                {'error': f'Erro ao deletar perfil: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
