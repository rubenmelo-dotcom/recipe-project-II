from tests.functional_tests.recipes.functional_base_test import RecipeFunctionalBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from recipes.tests.recipe_base_test import RecipeMixin
from unittest.mock import patch
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.functional_test
class RecipeHomePageTest(RecipeFunctionalBaseTest, RecipeMixin):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        msg = 'Nenhum receita publicada. Volte mais tarde.'
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(
            By.TAG_NAME,
            'body'
        )
        self.assertIn(msg, body.text)

    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self._make_recipe_at_scale(3)
        title_needed = 'This is what i need'
        recipes[0].title = title_needed
        recipes[0].save()

        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(
            By.NAME,
            'search'
        )

        search_input.send_keys(title_needed[:7])
        search_input.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, 'recipe'),
                title_needed
            )
        )

        recipe = self.browser.find_element(
            By.CLASS_NAME, 'recipe'
        )

        self.assertIn(title_needed, recipe.text)
