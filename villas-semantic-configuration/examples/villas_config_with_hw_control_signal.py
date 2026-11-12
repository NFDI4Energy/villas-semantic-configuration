from pathlib import Path

from vsc.convert import get_semantic_representation


def main():
    example_file = Path(__file__).parent / 'villas_config_with_hw_control_signal.json'
    body = example_file.read_bytes()
    output = get_semantic_representation(body, 'text/turtle')
    target_file = example_file.with_suffix('.ttl')
    target_file.write_bytes(output)


if __name__ == "__main__":
    main()
