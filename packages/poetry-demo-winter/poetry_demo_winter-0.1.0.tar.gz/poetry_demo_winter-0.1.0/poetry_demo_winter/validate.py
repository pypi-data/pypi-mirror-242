import argparse

from dotenv import dotenv_values

from poetry_demo_winter.numlookupapi import PhoneNumberValidator


env_config = dotenv_values()

def main():
    import os
    print(os.getcwd())
    api_key = env_config['NUMLOOKUPAPI_KEY']
    validator = PhoneNumberValidator(api_key=api_key)

    parser = argparse.ArgumentParser(
        prog='PhoneValidatorCLI.',
        description='CLI utility for phone numbers validation check.',
        epilog='Thanks!'
    )
    parser.add_argument('--phone-number', '-pn', type=str, help='Phone number for checking')
    parser.add_argument('--country-code', '-cc', type=str, help='Country code')
    args = parser.parse_args()

    country_code_part = ' with country code: ' + args.country_code if args.country_code is not None else ''
    main_part = f"Phone number {args.phone_number}{country_code_part} is"

    if validator.validate(args.phone_number, args.country_code):
        print(f"{main_part} valid.")
    else:
        print(f"{main_part} invalid.")


if __name__ == "__main__":
    main()
