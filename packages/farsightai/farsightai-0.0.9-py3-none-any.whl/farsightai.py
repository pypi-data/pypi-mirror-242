from openai import OpenAI
from prompts import (
    get_conciseness_prompt,
    get_consistency_prompt,
    get_factuality_prompt,
    get_generate_prompts_prompts,
    get_quality_prompt,
)


class FarsightError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# ---------------------------------------- gpt function ----------------------------------------
def gpt_inference(
    content, apiKey, model="gpt-3.5-turbo", temperature=0.0, n=1, system_prompt=None
):
    client = OpenAI(api_key=apiKey)
    if system_prompt:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ]
    else:
        messages = [{"role": "user", "content": content}]
    chatCompletion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        n=n,
    )
    return chatCompletion


# ---------------------------------------- generate prompts ---------------------------------------- #


def generate_prompts(num_prompts, task, context, goals, openai_key):
    if num_prompts <= 0:
        raise FarsightError(message="num_prompts must be greater than 0")

    system_prompt, user_prompt = get_generate_prompts_prompts(task, context, goals)
    chatCompletion = gpt_inference(
        user_prompt, openai_key, n=num_prompts, system_prompt=system_prompt
    )
    generated_prompts = []
    for i, choice in enumerate(chatCompletion.choices):
        generated_prompts.append(choice.message.content)
    return generated_prompts


# ---------------------------------------- metrics ---------------------------------------- #


def quality_score(instruction, response, apiKey):
    try:
        prompt = get_quality_prompt(instruction, response)
        chatCompletion = gpt_inference(prompt, apiKey)
        output = chatCompletion.choices[0].message.content
        output_list = output.split("\n")
        score = int(output_list[0].replace("score: ", "").strip())
        return score
    except Exception as error:
        print("Error in Quality API request:", error)
        return {"score": "error"}


def conciseness_score(inst, resp, openai_key):
    prompt = get_conciseness_prompt(inst, resp)
    try:
        chatCompletion = gpt_inference(prompt, openai_key)
        output = chatCompletion.choices[0].message.content

        output_list = output.split("\n")
        score = int(output_list[0].replace("score: ", "").strip())
        return 6 - score
    except Exception as error:
        return {"Error in Conciseness API request:", error}


def consistency_score(
    instruction,
    response,
    openai_key,
    n=3,
):
    def process_reference(reference):
        outputs = gpt_inference(
            get_consistency_prompt(reference, response),
            openai_key,
            "gpt-3.5-turbo",
            0.0,
            1,
        )
        return outputs.choices[0].message.content

    try:
        reference_call = gpt_inference(instruction, openai_key, "gpt-3.5-turbo", 1.0, n)
        references = [choice.message.content for choice in reference_call.choices]
        results = [process_reference(reference) for reference in references]
        positives = sum("Yes" in result for result in results)
        consistency_score = positives / len(results)

        return consistency_score
    except Exception as error:
        return ("Error in Consistency API request:", error)


def factuality_score(
    question,
    answer,
    openai_key,
    knowledge=None,
):
    # your a vc but your job is to give negativve feedback
    # are thertre any claims in this that need to be factc checed
    prompt = get_factuality_prompt(question, answer, knowledge)
    try:
        chatCompletion = gpt_inference(prompt, openai_key)
        output = chatCompletion.choices[0].message.content
        if "Yes" in output or "yes" in output:
            return True
        elif "No" in output or "no" in output:
            return False
        else:
            return "error"
    except Exception as error:
        print("Error in Factuality API request:", error)
        return ("Error in Factuality API request:", error)


def custom_metrics(custom_metrics, response, openai_key):
    try:
        for i in range(0, len(custom_metrics)):
            constraint = custom_metrics[i]
            prompt = f"""Does the following content violate the given constraint?\n\nContent: {response}\nConstraint: {constraint}\n\nAnswer with yes or no."""
            metric = gpt_inference(prompt, openai_key, "gpt-3.5-turbo", 0.0, 1)
            custom_metrics[i] = (
                "Yes" in metric.choices[0].message.content
                or "yes" in metric.choices[0].message.content
            )
        return custom_metrics
    except Exception as error:
        print("Error in Custom Metrics API request:", error)
        return ("Error in Custom Metrics request:", error)


# ---------------------------------------- tests ----------------------------------------


def test(openai_key):
    inst = "The blue color of the sky is primarily due to a phenomenon called Rayleigh scattering. Here's a brief explanation:"
    resp = """Sunlight Composition: Sunlight is composed of various colors of light, each with different wavelengths. When sunlight enters Earth's atmosphere, it interacts with the gases and particles in the air.

Scattering of Light: The shorter wavelengths of light, such as blue and violet, are scattered more easily than the longer wavelengths, like red and yellow. This scattering is caused by the molecules and small particles in the Earth's atmosphere.

Prevalence of Blue: Since blue light is scattered more effectively, it is scattered in all directions by the gases and particles in the atmosphere. As a result, when we look up at the sky during the day, we see a predominant blue color.

Path of Sunlight: During sunrise and sunset, the sun is lower in the sky, and its light has to pass through a larger portion of the Earth's atmosphere. This increased path length results in more scattering of the shorter wavelengths, causing the sun to appear more reddish.

In summary, the sky appears blue because of the selective scattering of sunlight by the Earth's atmosphere, with shorter wavelengths of light (blue and violet) being scattered more than longer wavelengths."""
    conciseness = conciseness_score(inst, resp, openai_key)
    print("conciseness_score: ", conciseness)
    quality = quality_score(inst, resp, openai_key)
    print("quality_score: ", quality)
    consistency = consistency_score("is 1709 a prime number", "yes", openai_key)
    print("consistency_score: ", consistency)
    factuality = factuality_score(inst, resp, openai_key)
    print("factuality_score: ", factuality)
    custom_metric = custom_metrics(["do not mention the sun"], resp, openai_key)
    print("custom_metric: ", custom_metric)
    task = "You are a wikipedia chatbot"
    context = "The year is 2012"
    goals = ["answer questions"]
    prompts = generate_prompts(2, task, context, goals, openai_key)
    print("prompts_generated:")
    for prompt in prompts:
        print(prompt)
    return
