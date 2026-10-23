# transactions/management/commands/seed_accounts.py
from django.core.management.base import BaseCommand
from transactions.models import Account
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed the database with 5 test accounts (A1001-A1005) with 1000 balance each'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing accounts before seeding',
        )

    def handle(self, *args, **options):
        if options['reset']:
            deleted_count, _ = Account.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted_count} existing account(s).'))

        accounts_data = [
            {'account_number': 'A1001', 'balance': Decimal('1000.00')},
            {'account_number': 'A1002', 'balance': Decimal('1000.00')},
            {'account_number': 'A1003', 'balance': Decimal('1000.00')},
            {'account_number': 'A1004', 'balance': Decimal('1000.00')},
            {'account_number': 'A1005', 'balance': Decimal('1000.00')},
        ]

        created_count = 0
        updated_count = 0

        for data in accounts_data:
            account, created = Account.objects.update_or_create(
                account_number=data['account_number'],
                defaults={'balance': data['balance'], 'is_active': True}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✅ Created {account.account_number} with balance {account.balance}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'  ⚠️  Updated {account.account_number} to balance {account.balance}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created: {created_count}, Updated: {updated_count}'
        ))