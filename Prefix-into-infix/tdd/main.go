package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func isOperator(token string) bool {
	return token == "+" || token == "-" || token == "*" || token == "/"
}

func isNumber(token string) bool {
	_, err := strconv.ParseFloat(token, 64)
	return err == nil
}

func toInfix(tokens []string) (string, []string, error) {
	if len(tokens) == 0 {
		return "", []string{}, fmt.Errorf("пустое выражение")
	}

	token := tokens[0]
	tokens = tokens[1:]

	if isNumber(token) {
		return token, tokens, nil
	}

	if !isOperator(token) {
		return "", []string{}, fmt.Errorf("недопустимый токен: %s", token)
	}

	if len(tokens) < 2 {
		return "", []string{}, fmt.Errorf("недостаточно операндов для оператора %s", token)
	}

	leftOperand, tokens, err := toInfix(tokens)
	if err != nil {
		return "", []string{}, err
	}

	rightOperand, tokens, err := toInfix(tokens)
	if err != nil {
		return "", []string{}, err
	}

	infixExpression := "(" + leftOperand + " " + token + " " + rightOperand + ")"

	return infixExpression, tokens, nil
}

func processInput() (string, error) {
	scanner := bufio.NewScanner(os.Stdin)
	fmt.Print("Введите выражение в префиксной нотации: ")
	scanner.Scan()
	input := scanner.Text()

	tokens := strings.Fields(input)
	infixExpression, remainingTokens, err := toInfix(tokens)

	if err != nil {
		return "", err
	} else if len(remainingTokens) == 0 {
		return infixExpression, nil
	} else {
		return "", fmt.Errorf("Недопустимое выражение")
	}
}

func main() {
	result, err := processInput()
	if err != nil {
		fmt.Println("Ошибка:", err)
	} else {
		fmt.Println("Инфиксная запись выражения:", result)
	}
}
