package main

import (
	"strings"
	"testing"
)

func TestToInfix(t *testing.T) {
	tests := []struct {
		input    string
		expected string
		err      bool
	}{
		{"+ - 13 4 55", "((13 - 4) + 55)", false},
		{"+ 2 * 2 - 2 1", "(2 + (2 * (2 - 1)))", false},
		{"+ + 10 20 30", "((10 + 20) + 30)", false},
		{"- - 1 2", "", true}, // Неправильное выражение
		{"/ + 3 10 * + 2 3 - 3 5", "((3 + 10) / ((2 + 3) * (3 - 5)))", false},
	}

	for _, test := range tests {
		t.Run(test.input, func(t *testing.T) {
			tokens := strings.Fields(test.input)
			result, _, err := toInfix(tokens)

			if err != nil && !test.err {
				t.Errorf("Для входных данных '%s' ожидалась успешная конвертация, но получено сообщение об ошибке: %v", test.input, err)
			}

			if err == nil && test.err {
				t.Errorf("Для входных данных '%s' ожидалась ошибка, но конвертация прошла успешно: %s", test.input, result)
			}

			if result != test.expected {
				t.Errorf("Для входных данных '%s' получено неверное выражение. Ожидается: %s, получено: %s", test.input, test.expected, result)
			}
		})
	}
}
