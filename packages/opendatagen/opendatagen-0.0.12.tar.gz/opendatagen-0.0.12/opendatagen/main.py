from opendatagen.template import Template, TemplateManager, TemplateName, Variable
from opendatagen.data_generator import DataGenerator
from opendatagen.model import LLM, ModelName
from opendatagen.anonymizer import Anonymizer
from opendatagen.utils import find_strings_in_brackets, snake_case_to_title_case
from opendatagen.agent import DataAgent

def anonymize_text(): 

    text_to_anonymize = """
            My name is Thomas, Call me at 0601010129 or email me at john.doe@example.com. 
            My SSN is 123-45-6789 and 4242 4242 8605 2607 is my credit card number. 
            Living in the best city in the world: Melbourne.
            New York & Co is a restaurant.
            It is 10 am.
            I have 10€ in my pocket. Oh my god.
            I have park my Tesla next to your house.
            My id is 0//1//2//2//2//2
    """
    
    completion_model = LLM.load_chat.GPT_4_TURBO_CHAT

    anonymizer = Anonymizer(completion_model=completion_model)

    anonymized_text = anonymizer.anonymize(text=text_to_anonymize)
    
    print(anonymized_text)

def generate_data_from_predefined_template(): 
    
    variation_model = LLM.load_chat.GPT_4_TURBO_CHAT
    completion_model = LLM.load_chat.GPT_4_TURBO_CHAT
    
    manager = TemplateManager()
    template = manager.get_template(TemplateName.CHUNK)

    if template:

        generator = DataGenerator(template=template, variation_model=variation_model, completion_model=completion_model)
        
        data = generator.generate_data(output_path="output.csv")
        
        print(data)
    
def generate_data_from_user_defined_template():    

    variation_model = LLM.load_chat.GPT_4_TURBO_CHAT 
    completion_model = LLM.load_instruct.GPT_35_TURBO_INSTRUCT

    # Create the custom template using the Pydantic models
    user_template = Template(
        description="Custom template for Python exercises",
        prompt="Python exercice statement: {python_exercice_statement}",
        completion="Answer:\n{python_code}",
        prompt_variation_number=1,
        prompt_variables={
            "python_exercice_statement": Variable(
                name="Python exercice statement",
                temperature=1,
                max_tokens=120,
                generation_number=10
            )
        },
        completion_variables={
            "python_code": Variable(
                name="Python code",
                temperature=0,
                max_tokens=256,
                generation_number=1
            )
        }
    )

    generator = DataGenerator(template=user_template, variation_model=variation_model, completion_model=completion_model)
    
    data = generator.generate_data(output_path="output.csv")

    print(data)


def generate_variation_from_variable():

    variation_model = LLM.load_chat.GPT_4_TURBO_CHAT
    completion_model = LLM.load_instruct.TEXT_DAVINCI_INSTRUCT

    manager = TemplateManager()
    template = manager.get_template(TemplateName.PRODUCT_REVIEW)

    generator = DataGenerator(template=template, variation_model=variation_model, completion_model=completion_model)

    prompt = template.prompt 
    #prompt = Write a review of '{product_name}' made by {brand}:
    prompt_variables = generator.extract_variable_from_string(prompt) 

    prompts_parameters = generator.contextual_prompt_generation(prompt=prompt, 
                                                                variables=prompt_variables, 
                                                                current_variation_dict={}, 
                                                                fixed_variables=template.prompt_variables)
    
    print(prompts_parameters)

if __name__ == "__main__":

    agent = DataAgent()
    
    agent.run()
    #anonymize_text()
    #generate_data_from_predefined_template()

    #generate_data_from_user_defined_template()

    #generate_variation_from_variable()
    