
from purepyhome.core.signals.get_entity import get_entity_over_signal
from purepyhome.core.signals.update_entity import update_entity_over_signal

class ActionsPhraser:
    def __init__(self):
        self.temp_vars = {}
        self.value = None
        self.call_stack_of_entitie_handler = []

    def solve_variable_get(self, variable: str) -> str:

        # check if the variable is a string/constant
        if variable[0] == "'" and variable[-1] == "'":
            return variable[1:-1]
        
        # check if the variable is a temp variable
        if variable[0] == '$':
            if variable in self.temp_vars:
                return self.temp_vars[variable]
            else:
                raise Exception(f'Variable {variable} not found')
            
        # check if the variable is the value of the entity
        if variable == 'value':
            return self.value
        
        # check if the variable is the value of an other entity
        else:
            return get_entity_over_signal(variable).value


    def solve_variable_set(self, variable: str, value: str) -> None:

        # check if the variable is a temp variable
        if variable[0] == '$':
            self.temp_vars[variable] = value

        # check if the variable is the value of the entity
        else:
            update_entity_over_signal(__name__, entity_id=variable, value=value, callstack=self.call_stack_of_entitie_handler)


    def evaluate_condition(self, condition_str: str, depth=0) -> bool:
        # devide the condition string into parts
        parts = condition_str.split(' ')
        
        # try to devide at OR or AND and evaluate the parts
        if 'OR' in parts:
            index = parts.index('OR')
            left = parts[:index]
            right = parts[index+1:]
            res = self.evaluate_condition(' '.join(left), depth=depth+1) or self.evaluate_condition(' '.join(right), depth=depth+1)
            return res
        elif 'AND' in parts:
            index = parts.index('AND')
            left = parts[:index]
            right = parts[index+1:]
            res = self.evaluate_condition(' '.join(left), depth=depth+1) and self.evaluate_condition(' '.join(right), depth=depth+1)
            return res
        
        # if no OR or AND is found...
        # try devide at operator (<, >, == etc)
        operators = ['<', '>', '<=', '>=', '==', '!=']
        current_operator = None
        index = None
        for operator in operators:
            if operator in parts:
                current_operator = operator
                index = parts.index(operator)
                break

        # if an operator is found, evaluate the parts
        if current_operator:
            leftstr = ''.join(parts[:index])
            rightstr = ''.join(parts[index+1:])
            left = self.solve_variable_get(leftstr)
            right = self.solve_variable_get(rightstr)
            self.logger.debug(f'action_phraser:::{"  " * depth} - var: {leftstr} -> {left}')
            self.logger.debug(f'action_phraser:::{"  " * depth} - var: {rightstr} -> {right}')
            if current_operator == '<':
                result = True if left < right else False
            elif current_operator == '>':
                result = True if left > right else False
            elif current_operator == '<=':
                result = True if left <= right else False
            elif current_operator == '>=':
                result = True if left >= right else False
            elif current_operator == '==':
                result = True if left == right else False
            elif current_operator == '!=':
                result = True if left != right else False
            return result
        else:
            raise Exception('Invalid condition')


    def evaluate_if(self, if_yaml: dict, depth=0):
        self.logger.debug(f'action_phraser:::{"  " * depth} Evaluating if:')

        # get the condition and evaluate it
        if 'condition' in if_yaml:
            condition = if_yaml['condition']
            self.logger.debug(f'action_phraser:::{"  " * depth} - Checking condition: {condition}')
            res = self.evaluate_condition(condition)
            self.logger.debug(f'action_phraser:::{"  " * depth} - Condition result: {res}')

            # if the condition is true, try to run the then part
            if res:
                if 'then' in if_yaml:
                    self.phrase_action(if_yaml['then'], depth=depth+1)

            # if the condition is false, try to run the else part
            else:
                if 'else' in if_yaml:
                    self.phrase_action(if_yaml['else'], depth=depth+1)


    def evaluate_set(self, set_str: str, depth=0):
        self.logger.debug(f'action_phraser:::{"  " * depth} Evaluating set: {set_str}')

        parts = set_str.split(' ')

        # check if the set statement has a '=', else the statement is invalid
        if parts.count('=') == 1:
            variable = parts[0]
            value = parts[2:]
        else:
            raise Exception('Invalid set statement')
        
        # solve the value and set the variable
        value = self.solve_variable_get(''.join(value))
        self.solve_variable_set(variable, value)


    def phrase_action(self, action_yaml: dict, depth = 0) -> bool:
        self.logger.debug(f'action_phraser:::{"  " * depth} Running action:')
        for step in action_yaml:
            try:
                if next(iter(step)) == 'set':
                    self.evaluate_set(step['set'], depth=depth+1)
                elif next(iter(step)) == 'if':
                    self.evaluate_if(step['if'], depth=depth+1)
            except Exception as e:
                self.logger.error(f'action_phraser:::{"  " * depth} Error: {e}')
                return False
        return True


    def setup(self, logger, value: str, call_stack: list = []):
        self.logger = logger
        self.value = value
        self.call_stack_of_entitie_handler = call_stack
            
