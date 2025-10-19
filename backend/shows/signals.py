from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Show, Performance
from logzero import logger


@receiver(post_save, sender=Show)
def clear_show_cache(sender, instance, **kwargs):
    logger.info(f"Delete cache for show ID: {instance.id}")
    cache.delete('shows_list')
    cache.delete(f'show_detail_{instance.id}')


@receiver(post_save, sender=Performance)
def clear_performance_related_cache(sender, instance, **kwargs):
    logger.info(f"Delete cache Performance ID: {instance.id}")
    if instance.show:
        clear_show_cache(sender=Show, instance=instance.show)
