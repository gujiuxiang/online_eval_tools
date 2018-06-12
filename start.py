from flask import Flask, render_template, url_for, request, redirect
import os, os.path
import json

ip_address = "xxx.xxx.xxx.xxx"

app = Flask(__name__)
dataset = json.load(open('coco_caption_C.json'))
c_dataset = json.load(open('coco_caption_human_eval.json'))
cu_dataset = json.load(open('coco_caption_human_eval_upper.json'))
cg_dataset = json.load(open('coco_caption_human_eval_gt.json'))
img_ids = dataset['img_ids']
img_id2QAs = dataset['img_id2QAs']
img_id2captions = dataset['img_id2captions']
img_id2split = dataset['img_id2split']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/redirect_user')
def redirect_user():
    for uid in range(0,20):
        user_result_dir = './users/u%d/result/'%uid
        if len(os.listdir(user_result_dir))==0 and not os.path.exists('./users/u%d/on_hold.json'%(uid)):
            with open('./users/u%d/on_hold.json'%(uid), 'w') as outfile:
                json.dump([1], outfile)
            return redirect('http://xxx.xx.xx.xxx:5000/%d'%uid)
    return redirect('http://xxx.xx.xx.xxx:5000/thanks')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/<int:uid>', methods=['GET', 'POST'])

def start(uid):
    im_q_list = json.load(open('./users/u%d/im_c_list.json' % (uid)))
    if request.method == 'POST':
        print 'saving --- '
        fluent = request.form['fluent']
        correct = request.form['correct']
        fluent_u = request.form['fluent_u']
        correct_u = request.form['correct_u']
        fluent_g = request.form['fluent_g']
        correct_g = request.form['correct_g']
        imid = request.form['imid']
        qid = request.form['qid']
        question_type = request.form['question_type']
        print '<%s,%s,%s>'%(imid,qid,question_type)
        result = {'imid': int(imid), 'qid': int(qid), 'fluent_score': int(fluent), 'correct_score': int(correct),
                  'fluent_score_u': int(fluent_u), 'correct_score_u': int(correct_u),
                  'fluent_score_g': int(fluent_g), 'correct_score_g': int(correct_g)}
        print('./users/u%d/result/%d_%d.json' % (uid, int(imid), int(qid)))
        with open('./users/u%d/result/%d_%d.json'%(uid,int(imid),int(qid)), 'w') as outfile:
            json.dump(result, outfile)

        print request.form

    user_result_dir = './users/u%d/result/'%uid
    postid = len(os.listdir(user_result_dir))
    if postid==len(im_q_list):
        return redirect('http://xxx.xx.xx.xxx:5000/thanks')
    print 'loading --- '
    imid =im_q_list[postid][0]
    qid = im_q_list[postid][1]
    img_folder = 'static/cocodata'
    split = img_id2split[str(imid)]
    imfile  = r'%s/%s2014/COCO_%s2014_%012d.jpg'%(img_folder, split, split, int(imid))
    qae = img_id2QAs[str(imid)][qid]
    question = qae['question']
    question_type = qae['question_type']
    print '<%s,%s,%s>'%(imid,qid,question_type)
    answer = qae['multiple_choice_answer']
    explanation = c_dataset[str(imid)]
    explanation_u = cu_dataset[str(imid)]
    explanation_g = cg_dataset[str(imid)]
    print 'uid--', uid
    prog = int(float(postid)/len(im_q_list)*100)
    print 'prog--',prog
    return render_template('start.html',imfile=imfile, question=question,
    answer=answer,explanation=explanation,explanation_u=explanation_u, explanation_g=explanation_g, imid=imid,qid=qid,postid=postid,question_type=0,prog=prog)
