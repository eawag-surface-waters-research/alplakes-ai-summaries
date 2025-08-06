import argparse
import functions as f
from any_llm import completion

def main(params):
    function = getattr(f, params["function"])  # same as f.test
    response = completion(
        model=params["model"],
        messages=[{"role": "user", "content": function(params["parameter"])}],
        api_key=params["api_key"]
    )
    output = response.choices[0].message.content
    print(output)
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', help="LLM to use for request", type=str, required=True)
    parser.add_argument('--api_key', '-k', help="LLM API key", type=str, required=True)
    parser.add_argument('--function', '-f', help="Model input generation function name", type=str, required=True)
    parser.add_argument('--parameter', '-p', help="Text parameter to pass to generation function", type=str, required=True)
    args = parser.parse_args()
    params = vars(args)
    main(params)