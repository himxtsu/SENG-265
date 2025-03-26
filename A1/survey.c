#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 3000
#define MAX_TOKENS 3000 // Adjust based on expected number of tokens
#define MAX_RESPONSES 5  // Maximum number of responses expected
#define MAX_RESPONSE_ITEMS 100 // Maximum items per response

// arrays for each element in the input
char bits[MAX_TOKENS][MAX_LINE_LENGTH];
char questions[MAX_TOKENS][MAX_LINE_LENGTH];
char directreverse[MAX_TOKENS][MAX_LINE_LENGTH];
char likerts[MAX_TOKENS][MAX_LINE_LENGTH];
char responses[MAX_RESPONSES][MAX_RESPONSE_ITEMS][MAX_LINE_LENGTH]; // Store responses

// makes comparisons easier
char fully_disagree_str[MAX_LINE_LENGTH] = "fully disagree";
char disagree_str[MAX_LINE_LENGTH] = "disagree";
char partially_disagree_str[MAX_LINE_LENGTH] = "partially disagree";
char partially_agree_str[MAX_LINE_LENGTH] = "partially agree";
char agree_str[MAX_LINE_LENGTH] = "agree";
char fully_agree_str[MAX_LINE_LENGTH] = "fully agree";
char scores[MAX_RESPONSE_ITEMS][MAX_LINE_LENGTH];

double C_total = 0;
double I_total = 0;
double G_total = 0;
double U_total = 0;
double P_total = 0;

void readConfigFromStdin() {
    char line[MAX_LINE_LENGTH];
    int bitIndex = 0, questionIndex = 0, directReverseIndex = 0, likertIndex = 0;
    int responseIndex = 0; // To store the responses

    // Read from standard input line by line
    while (fgets(line, sizeof(line), stdin)) {
        // Ignore lines that start with '#'
        if (line[0] == '#') {
            continue;
        }

        // Trim newline character
        line[strcspn(line, "\n")] = 0;

        // Tokenize based on specific delimiters
        if (bitIndex == 0) { // First line (bits)
            char *token = strtok(line, ",");
            while (token != NULL && bitIndex < MAX_TOKENS) {
                strcpy(bits[bitIndex++], token);
                token = strtok(NULL, ",");
            }
        } else if (questionIndex == 0 && line[0] != '\0') { // Questions line
            char *token = strtok(line, ";");
            while (token != NULL && questionIndex < MAX_TOKENS) {
                strcpy(questions[questionIndex++], token);
                token = strtok(NULL, ";");
            }
        } else if (directReverseIndex == 0 && line[0] != '\0') { // Direct/Reverse line
            char *token = strtok(line, ";");
            while (token != NULL && directReverseIndex < MAX_TOKENS) {
                strcpy(directreverse[directReverseIndex++], token);
                token = strtok(NULL, ";");
            }
        } else if (likertIndex == 0 && line[0] != '\0') { // Likert items line
            char *token = strtok(line, ",");
            while (token != NULL && likertIndex < MAX_TOKENS) {
                strcpy(likerts[likertIndex++], token);
                token = strtok(NULL, ",");
            }
        } else if (responseIndex < MAX_RESPONSES) { // Responses
            char *token = strtok(line, ",");
            int responseSubIndex = 0; // To keep track of the response entry
            
            // Ignore the first three entries
            while (token != NULL && responseSubIndex < MAX_RESPONSE_ITEMS) {
                if (responseSubIndex >= 3) { // Store only after ignoring the first 3
                    strcpy(responses[responseIndex][responseSubIndex - 3], token);
                }
                token = strtok(NULL, ",");
                responseSubIndex++;
            }
            responseIndex++; // Move to the next response after one is stored
        }
    }
}

int mapLikertToScore(char* response, int isReverse) {
    int score = 0;

    // Map responses to corresponding values
    if (strcmp(response, fully_disagree_str) == 0) {
        score = isReverse ? 6 : 1;
    } else if (strcmp(response, disagree_str) == 0) {
        score = isReverse ? 5 : 2;
    } else if (strcmp(response, partially_disagree_str) == 0) {
        score = isReverse ? 4 : 3;
    } else if (strcmp(response, partially_agree_str) == 0) {
        score = isReverse ? 3 : 4;
    } else if (strcmp(response, agree_str) == 0) {
        score = isReverse ? 2 : 5;
    } else if (strcmp(response, fully_agree_str) == 0) {
        score = isReverse ? 1 : 6;
    }
    
    return score;
}

void calculateAndPrintScores(int responseIndex, double* C_avg, double* I_avg, double* G_avg, double* U_avg, double* P_avg) {
    // C, I, G, U, P question indices
    int C_questions[] = {0, 1, 2, 3, 4, 5, 6, 7}; // C1-C10 (indices)
    int I_questions[] = {8, 9, 10, 11, 12, 13, 14, 15, 16, 17}; // I1-I10
    int G_questions[] = {18, 19, 20, 21, 22, 23, 24, 25, 26, 27}; // G1-G15
    int U_questions[] = {28, 29, 30, 31, 32, 33}; // U1-U8
    int P_questions[] = {34, 35, 36, 37}; // P2-P8

    // Totals for C, I, G, U, P
    double C_total = 0, I_total = 0, G_total = 0, U_total = 0, P_total = 0;

    // Calculate totals for C
    for (int i = 0; i < 8; i++) {
        int questionIndex = C_questions[i];
        int isReverse = strcmp(directreverse[questionIndex], "Reverse") == 0;
        C_total += mapLikertToScore(responses[responseIndex][questionIndex], isReverse);
    }

    // Calculate totals for I
    for (int i = 0; i < 10; i++) {
        int questionIndex = I_questions[i];
        int isReverse = strcmp(directreverse[questionIndex], "Reverse") == 0;
        I_total += mapLikertToScore(responses[responseIndex][questionIndex], isReverse);
    }

    // Calculate totals for G
    for (int i = 0; i < 10; i++) {
        int questionIndex = G_questions[i];
        int isReverse = strcmp(directreverse[questionIndex], "Reverse") == 0;
        G_total += mapLikertToScore(responses[responseIndex][questionIndex], isReverse);
    }

    // Calculate totals for U
    for (int i = 0; i < 6; i++) {
        int questionIndex = U_questions[i];
        int isReverse = strcmp(directreverse[questionIndex], "Reverse") == 0;
        U_total += mapLikertToScore(responses[responseIndex][questionIndex], isReverse);
    }

    // Calculate totals for P
    for (int i = 0; i < 4; i++) {
        int questionIndex = P_questions[i];
        int isReverse = strcmp(directreverse[questionIndex], "Reverse") == 0;
        P_total += mapLikertToScore(responses[responseIndex][questionIndex], isReverse);
    }

    // Calculate averages
    double C_avg_res = C_total / 8;
    double I_avg_res = I_total / 10;
    double G_avg_res = G_total / 10;
    double U_avg_res = U_total / 6;
    double P_avg_res = P_total / 4;

    // Print the results for this respondent
    printf("C:%.2f,I:%.2f,G:%.2f,U:%.2f,P:%.2f\n", C_avg_res, I_avg_res, G_avg_res, U_avg_res, P_avg_res);

    // Add to cumulative totals for overall averages
    *C_avg += C_avg_res;
    *I_avg += I_avg_res;
    *G_avg += G_avg_res;
    *U_avg += U_avg_res;
    *P_avg += P_avg_res;
}

void printSurveyOutput(int questionCount, int likertCount, int responseCount) {
    // Survey header
    printf("FOR EACH QUESTION BELOW, RELATIVE PERCENTUAL FREQUENCIES ARE COMPUTED FOR EACH LEVEL OF AGREEMENT\n\n");

    // Iterate through each question
    for (int i = 0; i < questionCount; i++) {
        printf("%s\n", questions[i]);
        // printf("%c\n", questions[i][0]);
       // printf("%s\n", directreverse[i]);

        // Store a current count of frequency for the current question
        double fully_disagree_count = 0;
        double disagree_count = 0;
        double partially_disagree_count = 0;
        double partially_agree_count = 0;
        double agree_count = 0;
        double fully_agree_count = 0;        
        
        // Print frequencies for each Likert item
        for (int j = 0; j < likertCount; j++) {
            for (int u = 0; u < responseCount; u++) {
                if (strcmp(responses[u][i], "fully disagree") == 0) {
                    fully_disagree_count += 1;
                }
                else if (strcmp(responses[u][i], "disagree") == 0) {
                    disagree_count += 1;      
                }
                else if (strcmp(responses[u][i], "partially disagree") == 0) {
                    partially_disagree_count += 1;         
                }            
                else if (strcmp(responses[u][i], "partially agree") == 0) {
                    partially_agree_count += 1;
                }            
                else if (strcmp(responses[u][i], "agree") == 0) {
                    agree_count += 1;          
                }            
                else if (strcmp(responses[u][i], "fully agree") == 0) {
                    fully_agree_count += 1;            
                }
                // snprintf(scores[u], MAX_LINE_LENGTH, "C:%.2f I:%.2f G:%.2f U:%.2f P:%.2f\n", C_total / 8, I_total / 10, G_total / 10, U_total / 6, P_total / 4);


            }       
            // printf("Yur: %.2f\n", fully_disagree_count);
            // printf("Yur: %.2f\n", disagree_count);
            // printf("Yur: %.2f\n", partially_disagree_count);
            // printf("Yur: %.2f\n", partially_agree_count);
            // printf("Yur: %.2f\n", agree_count);
            // printf("Yur: %.2f\n", fully_agree_count);

            if (strcmp(likerts[j], fully_disagree_str) == 0) {
                printf("%.2f: %s\n", fully_disagree_count / 5 * 100, likerts[j]);
            }
            else if (strcmp(likerts[j], disagree_str) == 0) {
                printf("%.2f: %s\n", disagree_count / 5 * 100, likerts[j]);
            }
            else if (strcmp(likerts[j],partially_disagree_str) == 0) {
                printf("%.2f: %s\n", partially_disagree_count / 5 * 100, likerts[j]);
            }
            else if (strcmp(likerts[j], partially_agree_str) == 0) {
                printf("%.2f: %s\n", partially_agree_count / 5 * 100, likerts[j]);
            }
            else if (strcmp(likerts[j], agree_str) == 0) {
                printf("%.2f: %s\n", agree_count / 5 * 100, likerts[j]);
            }
            else if (strcmp(likerts[j], fully_agree_str) == 0) {
                printf("%.2f: %s\n", fully_agree_count / 5 * 100, likerts[j]);
            }
            // printf("%.2f: %s\n", freq, likerts[j]);

            fully_disagree_count = 0;
            disagree_count = 0;
            partially_disagree_count = 0;
            partially_agree_count = 0;
            agree_count = 0;
            fully_agree_count = 0;   
        
        }

        // Only print a newline if this is not the last question
        if (i < questionCount - 1) {
            printf("\n");
        
        }  
    }
}


int main() {
    readConfigFromStdin();

    // Print the responses for debugging


    // Number of questions, likerts, and respondents
    int questionCount = 38; // Total questions from your input
    int likertCount = 6;    // 6 Likert items (fully disagree to fully agree)
    int responseCount = sizeof(responses) / sizeof(responses[0]);
    if (strcmp(bits[0], "1") == 0) {
        responseCount = 0;
    }
    double C_avg_total = 0, I_avg_total = 0, G_avg_total = 0, U_avg_total = 0, P_avg_total = 0;
    // double C_average = C_total / 8;
    // double I_average = I_total / 10;
    // double G_average = G_total / 10;
    // double U_average = U_total / 6;
    // double P_average = P_total / 4;
    printf("Examining Science and Engineering Students' Attitudes Towards Computer Science\n");
    printf("SURVEY RESPONSE STATISTICS\n\n");
    printf("NUMBER OF RESPONDENTS: %d\n\n", responseCount);
    // Output the formatted survey result
    if (strcmp(bits[0], "1") == 0 || strcmp(bits[1], "1") == 0 || strcmp(bits[3], "1") == 0) {
        printSurveyOutput(questionCount, likertCount, responseCount);
    }

    if (strcmp(bits[3], "1") == 0) {
        printf("\n");
    }
    
    if (strcmp(bits[2], "1") == 0) {
        printf("SCORES FOR ALL THE RESPONDENTS\n\n");        
        for (int i = 0; i < responseCount; i++) {
            // double C_avg_total = 0, I_avg_total = 0, G_avg_total = 0, U_avg_total = 0, P_avg_total = 0;
            calculateAndPrintScores(i, &C_avg_total, &I_avg_total, &G_avg_total, &U_avg_total, &P_avg_total);
        }        
    }

    if (strcmp(bits[3], "1") == 0) {
        // double C_avg_total = 0, I_avg_total = 0, G_avg_total = 0, U_avg_total = 0, P_avg_total = 0;

        // // Output the scores for each response and accumulate totals
        // for (int i = 0; i < responseCount; i++) {
        //     calculateAndPrintScores(i, &C_avg_total, &I_avg_total, &G_avg_total, &U_avg_total, &P_avg_total);
        // }

        // Calculate overall averages
        double C_avg_final = C_avg_total / responseCount;
        double I_avg_final = I_avg_total / responseCount;
        double G_avg_final = G_avg_total / responseCount;
        double U_avg_final = U_avg_total / responseCount;
        double P_avg_final = P_avg_total / responseCount;

        printf("\nAVERAGE SCORES PER RESPONDENT\n\n");
        printf("C:%.2f,I:%.2f,G:%.2f,U:%.2f,P:%.2f\n", C_avg_final, I_avg_final, G_avg_final, U_avg_final, P_avg_final);

    }
    // printResponses();
    // printf("C:%.2f I:%.2f G:%.2f U:%.2f P:%.2f\n", C_total / 8, I_total / 10, G_total / 10, U_total / 6, P_total / 4);
    return 0;
}
