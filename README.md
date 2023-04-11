
## Supplementary
### Task Description Overall 
for Section 3.2 Summary Quality Evaluator and Section 3.3 Summary Quality Improvement Rewriter
<img width="981" alt="Screen Shot 2023-04-10 at 3 12 28 PM" src="https://user-images.githubusercontent.com/129326702/230831059-de3a5c35-33e3-42b4-9cb0-81a9f4961b3a.png">

### User Study Survey Link for Section 4.3 Quality of Rewritten Summary (RQ2)
[https://forms.gle/gzSBoWSib9PqqTfw9](https://forms.gle/gzSBoWSib9PqqTfw9)

### Dataset Filtering and Sampling Details in Section 4.1 Dataset
Due to the training data for ‘gpt-3.5-turbo’ up to Sep 2021, we filter the bugs with bug summary rewriting (51,701 Mozilla bugs and 35,982 Eclipse bugs) in Section 2.2 by the bug creation time and only keep bugs with the bug creation time after ‘2021-10-01’ as our test
dataset to prevent data leakage. After filtering, we get 2,699 Mozilla bugs and 371 Eclipse bugs as our test bugs. We further filter these test bugs based on the bug description length (only keeping bugs with 10-300 tokens in the description) and the content of the bug
description (retaining bugs with descriptions primarily in natural language). Due to the LLM’s input length limitations, we do not process bugs with excessively long descriptions. Bugs with overly short descriptions are also removed, as they lack sufficient information. Regarding bug filtering based on description content, during the empirical study, we observe that bugs with bug descriptions
related to logs, stack traces or crash reports often follow project-specific conventions for their bug summary writing, which lack generalizability. As a result, we exclude these bugs from our test dataset, leaving us with 1,750 Mozilla bugs and 310 Eclipse bugs.

Since our research unit is summary pair, we transform the rest test bugs into test summary pairs (2,115 Mozilla summary pairs and 340 Eclipse summary pairs). Different from the empirical study for observing the motivation of change, for the bug with
more than once bug summary rewriting (𝑠𝑢𝑚𝑚𝑎𝑟𝑦0 → 𝑠𝑢𝑚𝑚𝑎𝑟𝑦1 → 𝑠𝑢𝑚𝑚𝑎𝑟𝑦2), we transform it into ⟨𝑠𝑢𝑚𝑚𝑎𝑟𝑦0, 𝑠𝑢𝑚𝑚𝑎𝑟𝑦2 ⟩ and ⟨𝑠𝑢𝑚𝑚𝑎𝑟𝑦1, 𝑠𝑢𝑚𝑚𝑎𝑟𝑦2 ⟩. Then, we use the final 𝑠𝑢𝑚𝑚𝑎𝑟𝑦2 in each summary pair as the ground truth summary, called reference.
In this work, we only study bug summary rewriting on three-aspect quality improvement, namely, specific, concise and easy-to-understand. Thus, we remove summary pairs changed for being sortable and up-to-date. We get 688 Mozilla summary pairs and 170
summary pairs left.

We sample 247 Mozilla summary pairs from 688 summary pairs to ensure the estimated accuracy in the samples with the error margin 0.05 at 95% confidence level. Then, we manually label 247 Mozilla and 170 Eclipse summary pairs for evaluating our approach.
The manual annotation process has two steps: for each summary pair ⟨𝑠𝑢𝑚𝑚𝑎𝑟𝑦0, 𝑠𝑢𝑚𝑚𝑎𝑟𝑦1⟩, first, we manually extract the specific five targets from the 𝑠𝑢𝑚𝑚𝑎𝑟𝑦0 for evaluating the extractor’s performance; Second, we find out the changes between 𝑠𝑢𝑚𝑚𝑎𝑟𝑦0 and
𝑠𝑢𝑚𝑚𝑎𝑟𝑦1. By these changes, we get the answers of questions in the discriminator, which are used for evaluating the discriminator.
During the manual annotation, we found that some non-bug’s summary pairs (such as task, enhancement) and unfiltered summary pairs related to being sortable and up-to-date in our dataset. Since we only focus on ‘bug’ summary rewriting, after removing these
summary pairs we get 159 Mozilla summary pairs and 63 Eclipse summary pairs as test dataset.

## Code Instruction
### The executable code scripts are in 'scripts' folder

1. python file 0 is dataset sampling for Empirical study in Section 2
2. python file 1 - 9 is instance labeling for BSIKG
3. python file 10 is BSIKG construction
4. python file 11 - 16 is test dataset filtering, sampling and labeling
5. python file 17 calculates bug summary length distribution
6. python 18_app_by_turbo is BSIAssist workflow
7. python file 19 - 20 is generation and rewriting baseline workflow
8. python file 21 - 22 is manual evaluation dataset sampling and user study survey generation 
9. python 23 - 25 is manual evaluation result processing

## Dataset Link
https://drive.google.com/file/d/1TpoFdle7G1YWdHRbm0l4xQEbuNV2-38M/view?usp=share_link
