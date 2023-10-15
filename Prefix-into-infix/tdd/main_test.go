package main

import (
	"os"
	"strings"
	"testing"
)

func TestIsOperator(t *testing.T) {
	tests := []struct {
		input    string
		expected bool
	}{
		{"+", true},
		{"-", true},
		{"*", true},
		{"/", true},
		{"%", false},
		{"=", false},
		{"1", false},
		{"abc", false},
		{"++", false},
		{"-+", false},
	}

	for _, test := range tests {
		t.Run(test.input, func(t *testing.T) {
			result := isOperator(test.input)

			if result != test.expected {
				t.Errorf("Для входного значения '%s' ожидалось %v, получено %v", test.input, test.expected, result)
			}
		})
	}
}

func TestIsNumber(t *testing.T) {
	tests := []struct {
		input    string
		expected bool
	}{
		{"123", true},
		{"-45", true},
		{"3.14", true},
		{"0.123", true},
		{"abc", false},
		{"++", false},
		{"-+", false},
		{"+", false},
		{"-", false},
		{"*", false},
		{"/", false},
	}

	for _, test := range tests {
		t.Run(test.input, func(t *testing.T) {
			result := isNumber(test.input)

			if result != test.expected {
				t.Errorf("Для входного значения '%s' ожидалось %v, получено %v", test.input, test.expected, result)
			}
		})
	}
}

func TestToInfix(t *testing.T) {
	tests := []struct {
		input    string
		expected string
		err      bool
	}{
		{"+ - 13 4 55", "((13 - 4) + 55)", false},
		{"+ 2 * 2 - 2 1", "(2 + (2 * (2 - 1)))", false},
		{"+ + 10 20 30", "((10 + 20) + 30)", false},
		{"- - 1 2", "", true},
		{"/ + 3 10 * + 2 3 - 3 5", "((3 + 10) / ((2 + 3) * (3 - 5)))", false},
		{"", "", true},
		{"1", "1", false},
		{"+ 1", "", true},
		{"++ 1 2", "", true},
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

func TestProcessInputValidExpression(t *testing.T) {
	testInput := "+ 2 3"
	expectedOutput := "(2 + 3)"

	r, w, _ := os.Pipe()
	os.Stdin = r
	defer func() {

	}()

	_, err := w.WriteString(testInput)
	if err != nil {
		t.Fatal(err)
	}
	w.Close()

	result, err := processInput()

	if err != nil {
		t.Errorf("Не ожидалась ошибка, но получена ошибка: %v", err)
	}

	if result != expectedOutput {
		t.Errorf("Ожидалось: %s, получено: %s", expectedOutput, result)
	}
}

func TestProcessInput(t *testing.T) {
	testCases := []struct {
		input    string
		expected string
		isError  bool
	}{
		{input: "+ 3 4", expected: "(3 + 4)", isError: false},
		{input: "недопустимый ввод", expected: "", isError: true},
		{input: "5 8 ,", expected: "", isError: true},
	}

	for _, testCase := range testCases {
		t.Run("Ввод: "+testCase.input, func(t *testing.T) {
			r, w, _ := os.Pipe()
			os.Stdin = r

			_, err := w.WriteString(testCase.input)
			if err != nil {
				t.Fatal(err)
			}
			w.Close()

			result, err := processInput()

			if testCase.isError && err == nil {
				t.Errorf("Ожидалась ошибка, но получено значение: %s", result)
			}

			if !testCase.isError && err != nil {
				t.Errorf("Ожидалось успешное выполнение, но получена ошибка: %v", err)
			}

			if result != testCase.expected {
				t.Errorf("Ожидалось: %s, получено: %s", testCase.expected, result)
			}
		})
	}
}
