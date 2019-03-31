from pattern.en import conjugate
import spacy
import textacy

try:
    conjugate(verb='go', tense='part')
except:
    pass


class Template:
    '''
    base:: string - a sentence template in the form of

    words words replaced words words replaced words replaced
    where replaced -> a token used to denote where a subject,
    object, or verb is placed.
    Default value of replaced is {}

    indexes:: dict - store order of bracket associated with
    subject, verb, object
    eg. {
        'subject': 0,
        'verb': 1,
        'object': 2,
    }

    This means subject in first bracket, verb in second etc.
    '''

    def __init__(self, base, indexes, replaced='{}'):
        self.base = base.split()
        self.indexes = indexes
        self.replaced = replaced
    
    def generate_sent(self, subject, action, obj):
        c = 0
        ans = []
        check_dict = {
            'subject': subject,
            'action': action,
            'object': obj,
        }

        for v in self.base:
            if v == self.replaced:
                for check in ['subject', 'action', 'object']:
                    if self.indexes[check] == c:
                        ans.append(check_dict[check])
                        break
                c += 1
            else:
                ans.append(v)

        # print('ans', ans)
        return ' '.join(ans)

class Generator:
    def __init__(self, sent, template):
        self.sent = sent
        self.template = template
        self.subject = ''
        self.action = ''
        self.object = ''
    
    def create_parts(self):
        parser = spacy.load('en_core_web_sm')
        parsed = parser(self.sent)
        vals = [
            [x.text for x in y] for y in 
            textacy.extract.subject_verb_object_triples(parsed)]

        if len(vals) > 0:
            self.subject, self.action, self.object = vals[0]
            self.action = conjugate(verb=self.action, tense='part')
            if self.action == 'being':
                self.action = ''

    def question(self):
        self.create_parts()
        return self.template.generate_sent(
                self.subject,
                self.action,
                self.object)


if __name__ == '__main__':
    base_template = 'Was {} not {} {} ?'
    base_index = {
        'subject': 0,
        'action': 1,
        'object': 2,
    }

    t = Template(base_template, base_index)
    print('Enter a line')
    line = input()
    g = Generator(line, t)
    print(g.question())