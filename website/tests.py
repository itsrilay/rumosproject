from django.test import TestCase
from django.contrib.auth.models import User
from .models import *


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)

    def test_user_authentication(self):
        user = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(user)

class CategoryModelTestCase(TestCase):
    def setUp(self):
        # Create some test categories
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')
    
    def test_category_creation(self):
        #Test that categories are created correctly.
        self.assertEqual(Category.objects.count(), 2)

    def test_category_str_representation(self):
        #Test the string representation of a category.
        self.assertEqual(str(self.category1), 'Category 1')
        self.assertEqual(str(self.category2), 'Category 2')

    def test_unique_category_names(self):
        #Test that category names are unique.
        duplicate_category = Category(name='Category 1')
        with self.assertRaises(Exception):
            duplicate_category.save()

class ProductModelTestCase(TestCase):
    def setUp(self):
        # Create a test category
        self.category = Category.objects.create(name='Test Category')
        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            price=19.99,
            description='This is a test product.',
        )

    def test_product_creation(self):
        #Test that products are created correctly.
        self.assertEqual(Product.objects.count(), 1)

    def test_product_str_representation(self):
        #Test the string representation of a product.
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_association_with_category(self):
        #Test that a product is associated with a category.
        self.assertEqual(self.product.category, self.category)

    def test_product_price_validation(self):
        #Test that the product price is valid.
        self.assertTrue(self.product.price > 0)

    def test_product_description(self):
        #Test the product description.
        self.assertEqual(self.product.description, 'This is a test product.')

class OrderModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.customer = Customer.objects.create(name='testname', email='testemail')
        # Create a test order
        self.order = Order.objects.create(customer=self.customer, complete=False, transaction_id='12345')

    def test_order_creation(self):
        #Test that orders are created correctly.
        self.assertEqual(Order.objects.count(), 1)

    def test_order_user_association(self):
        #Test that an order is associated with a user.
        self.assertEqual(self.order.customer, self.customer)

    def test_order_complete_status(self):
        #Test the order's complete status.
        self.assertFalse(self.order.complete)

    def test_order_transaction_id(self):
        #Test the order's transaction ID.
        self.assertEqual(self.order.transaction_id, '12345')

class OrderItemModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.customer = Customer.objects.create(name='testname', email='testemail')

        # Create a test category
        self.category = Category.objects.create(name='Test Category')

        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            price=19.99,
            description='This is a test product.',
        )

        # Create a test order
        self.order = Order.objects.create(customer=self.customer, complete=False, transaction_id='12345')

        # Create a test order item
        self.order_item = OrderItem.objects.create(product=self.product, order=self.order, quantity=2)

    def test_order_item_creation(self):
        #Test that order items are created correctly.
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_order_item_product_association(self):
        #Test that an order item is associated with a product.
        self.assertEqual(self.order_item.product, self.product)

    def test_order_item_order_association(self):
        #Test that an order item is associated with an order.
        self.assertEqual(self.order_item.order, self.order)

    def test_order_item_quantity(self):
        #Test the order item's quantity.
        self.assertEqual(self.order_item.quantity, 2)

    def test_order_item_total_price(self):
        #Test the order item's total price.
        self.assertEqual(self.order_item.get_total, 2 * self.product.price)

class AddressModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.customer = Customer.objects.create(name='testname', email='testemail')

        # Create a test address
        self.address = Address.objects.create(
            customer=self.customer,
            street='123 Test Street',
            city='Test City',
            postal_code='12345'
        )

    def test_address_creation(self):
        #Test that addresses are created correctly.
        self.assertEqual(Address.objects.count(), 1)

    def test_address_user_association(self):
        #Test that an address is associated with a user.
        self.assertEqual(self.address.customer, self.customer)

    def test_address_street(self):
        #Test the address street field.
        self.assertEqual(self.address.street, '123 Test Street')

    def test_address_city(self):
        #Test the address city field.
        self.assertEqual(self.address.city, 'Test City')

    def test_address_postal_code(self):
        #Test the address postal code field.
        self.assertEqual(self.address.postal_code, '12345')

class QuestionModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test question
        self.question = Question.objects.create(
            user=self.user,
            title='Test Question Title',
            body='This is a test question body.'
        )

    def test_question_creation(self):
        #Test that questions are created correctly.
        self.assertEqual(Question.objects.count(), 1)

    def test_question_user_association(self):
        #Test that a question is associated with a user.
        self.assertEqual(self.question.user, self.user)

    def test_question_title(self):
        #Test the question title field.
        self.assertEqual(self.question.title, 'Test Question Title')

    def test_question_body(self):
        #Test the question body field.
        self.assertEqual(self.question.body, 'This is a test question body.')

class AnswerModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test question
        self.question = Question.objects.create(
            user=self.user,
            title='Test Question Title',
            body='This is a test question body.'
        )

        # Create a test answer
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question,
            body='This is a test answer body.'
        )

    def test_answer_creation(self):
        #Test that answers are created correctly.
        self.assertEqual(Answer.objects.count(), 1)

    def test_answer_user_association(self):
        #Test that an answer is associated with a user.
        self.assertEqual(self.answer.user, self.user)

    def test_answer_question_association(self):
        #Test that an answer is associated with a question.
        self.assertEqual(self.answer.question, self.question)

    def test_answer_body(self):
        #Test the answer body field.
        self.assertEqual(self.answer.body, 'This is a test answer body.')

class ChallengeModelTestCase(TestCase):
    def setUp(self):
        # Create a test challenge
        self.challenge = Challenge.objects.create(
            text='Test Challenge Text',
            correct_answer='Test Correct Answer',
            date='2023-10-14'
        )

    def test_challenge_creation(self):
        #Test that challenges are created correctly.
        self.assertEqual(Challenge.objects.count(), 1)

    def test_challenge_text(self):
        #Test the challenge text field.
        self.assertEqual(self.challenge.text, 'Test Challenge Text')

    def test_challenge_correct_answer(self):
        #Test the correct answer field.
        self.assertEqual(self.challenge.correct_answer, 'Test Correct Answer')

    def test_challenge_date(self):
        #Test the challenge date field.
        self.assertEqual(self.challenge.date, '2023-10-14')