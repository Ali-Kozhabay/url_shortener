from django.core.management.base import BaseCommand
from accounts.models import Plan


class Command(BaseCommand):
    help = 'Initialize default pricing plans'

    def handle(self, *args, **options):
        plans_data = [
            {
                'name': 'free',
                'max_urls': 10,
                'max_clicks_per_month': 1000,
                'custom_alias': False,
                'analytics_retention_days': 30,
                'api_access': False,
                'price': 0
            },
            {
                'name': 'basic',
                'max_urls': 100,
                'max_clicks_per_month': 10000,
                'custom_alias': True,
                'analytics_retention_days': 90,
                'api_access': True,
                'price': 9.99
            },
            {
                'name': 'premium',
                'max_urls': 1000,
                'max_clicks_per_month': 100000,
                'custom_alias': True,
                'analytics_retention_days': 365,
                'api_access': True,
                'price': 29.99
            }
        ]

        for plan_data in plans_data:
            plan, created = Plan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created plan: {plan.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Plan already exists: {plan.name}")
                )
