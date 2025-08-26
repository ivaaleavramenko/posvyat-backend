import requests
from django.conf import settings

class BlackListService:
    def __init__(self):
        self.supabase_url = "https://mxqthiijfgxceyeufxpm.supabase.co/rest/v1/ЧС"
        self.headers = {
            "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14cXRoaWlqZmd4Y2V5ZXVmeHBtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTM3MDQ5NSwiZXhwIjoyMDcwOTQ2NDk1fQ.NQvvczctYMBpexHEydSmdC3glsdjaLQzMdGldFAVfrQ",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14cXRoaWlqZmd4Y2V5ZXVmeHBtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTM3MDQ5NSwiZXhwIjoyMDcwOTQ2NDk1fQ.NQvvczctYMBpexHEydSmdC3glsdjaLQzMdGldFAVfrQ",
            "Content-Type": "application/json"
        }
    
    def check_blacklist(self, first_name, last_name, middle_name=""):
        """Проверяет наличие человека в черном списке"""
        try:
            # Проверка в локальной БД
            from registration.models import BlackList
            local_match = BlackList.objects.filter(
                first_name__iexact=first_name,
                last_name__iexact=last_name
            )
            
            if local_match.exists():
                return True, "Найдено в локальной базе черного списка"
            
            # Проверка в Supabase
            params = {
                "select": "*",
                "Фамилия": f"ilike.*{last_name}*",
                "Имя": f"ilike.*{first_name}*"
            }
            
            if middle_name:
                params["Отчество"] = f"ilike.*{middle_name}*"
            
            response = requests.get(
                self.supabase_url,
                headers=self.headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    return True, f"Найдено в Supabase черном списке: {data[0].get('Причина', 'Причина не указана')}"
            
            return False, "Не найден в черных списках"
            
        except Exception as e:
            # В случае ошибки лучше заблокировать регистрацию
            return True, f"Ошибка проверки черного списка: {str(e)}"
    
    def sync_blacklist(self):
        """Синхронизирует черный список из Supabase в локальную БД"""
        try:
            response = requests.get(
                f"{self.supabase_url}?select=*",
                headers=self.headers
            )
            
            if response.status_code == 200:
                blacklist_data = response.json()
                
                for item in blacklist_data:
                    from registration.models import BlackList
                    BlackList.objects.update_or_create(
                        first_name=item.get('Имя', ''),
                        last_name=item.get('Фамилия', ''),
                        defaults={
                            'middle_name': item.get('Отчество', ''),
                            'vk_link': item.get('Ссылка на ВК', ''),
                            'reason': item.get('Причина', '')
                        }
                    )
                
                return True, f"Синхронизировано {len(blacklist_data)} записей"
            
            return False, "Ошибка получения данных из Supabase"
            
        except Exception as e:
            return False, f"Ошибка синхронизации: {str(e)}"
