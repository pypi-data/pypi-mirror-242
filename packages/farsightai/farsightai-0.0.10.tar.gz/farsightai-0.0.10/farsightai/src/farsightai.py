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


class FarsightAI:
    def __init__(self, openai_key):
        self.openai_key = openai_key

    # ---------------------------------------- generate prompts ---------------------------------------- #

    def generate_prompts(self, num_prompts, task, context, goals):
        if num_prompts <= 0:
            raise FarsightError(message="num_prompts must be greater than 0")

        system_prompt, user_prompt = get_generate_prompts_prompts(task, context, goals)
        chatCompletion = gpt_inference(
            user_prompt, self.openai_key, n=num_prompts, system_prompt=system_prompt
        )
        generated_prompts = []
        for i, choice in enumerate(chatCompletion.choices):
            generated_prompts.append(choice.message.content)
        return generated_prompts

    # ---------------------------------------- metrics ---------------------------------------- #

    def quality_score(self, instruction, response):
        try:
            prompt = get_quality_prompt(instruction, response)
            chatCompletion = gpt_inference(prompt, self.openai_key)
            output = chatCompletion.choices[0].message.content
            output_list = output.split("\n")
            score = int(output_list[0].replace("score: ", "").strip())
            return score
        except Exception as error:
            print("Error in Quality API request:", error)
            return {"score": "error"}

    def conciseness_score(self, inst, resp):
        prompt = get_conciseness_prompt(inst, resp)
        try:
            chatCompletion = gpt_inference(prompt, self.openai_key)
            output = chatCompletion.choices[0].message.content

            output_list = output.split("\n")
            score = int(output_list[0].replace("score: ", "").strip())
            return 6 - score
        except Exception as error:
            return {"Error in Conciseness API request:", error}

    def consistency_score(
        self,
        instruction,
        response,
        n=3,
    ):
        def process_reference(reference):
            outputs = gpt_inference(
                get_consistency_prompt(reference, response),
                self.openai_key,
                "gpt-3.5-turbo",
                0.0,
                1,
            )
            return outputs.choices[0].message.content

        try:
            reference_call = gpt_inference(
                instruction, self.openai_key, "gpt-3.5-turbo", 1.0, n
            )
            references = [choice.message.content for choice in reference_call.choices]
            results = [process_reference(reference) for reference in references]
            positives = sum("Yes" in result for result in results)
            consistency_score = positives / len(results)

            return consistency_score
        except Exception as error:
            return ("Error in Consistency API request:", error)

    def factuality_score(
        self,
        question,
        answer,
        knowledge=None,
    ):
        # your a vc but your job is to give negativve feedback
        # are thertre any claims in this that need to be factc checed
        prompt = get_factuality_prompt(question, answer, knowledge)
        try:
            chatCompletion = gpt_inference(prompt, self.openai_key)
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

    def custom_metrics(
        self,
        custom_metrics,
        response,
    ):
        try:
            for i in range(0, len(custom_metrics)):
                constraint = custom_metrics[i]
                prompt = f"""Does the following content violate the given constraint?\n\nContent: {response}\nConstraint: {constraint}\n\nAnswer with yes or no."""
                metric = gpt_inference(prompt, self.openai_key, "gpt-3.5-turbo", 0.0, 1)
                custom_metrics[i] = (
                    "Yes" in metric.choices[0].message.content
                    or "yes" in metric.choices[0].message.content
                )
            return custom_metrics
        except Exception as error:
            print("Error in Custom Metrics API request:", error)
            return ("Error in Custom Metrics request:", error)
