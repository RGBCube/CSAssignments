#include <stdio.h>

int main() {
    int ratings[21];
    int rating_frequency[] = {0, 0, 0, 0, 0};
    int rating_percent[] = {0, 0, 0, 0, 0};
    int total_stars = 0;

    for (int i = 0; i < 21; i++) {
        printf("Review number %i, enter rating (1 to 5): ", i+1);
        // read the input as int
        scanf("%i", &ratings[i]);

        int rating = ratings[i];

        if (rating < 1 || rating > 5) {
            fprintf(stderr, "Invalid rating! Ratings must be between 1 and 5.\n");
            return 1;
        }

        // increment the star count for the stars
        // (-1 is because indexes start from 0)
        ++rating_frequency[rating-1];
        total_stars += rating;
    }

    float average = (float) total_stars / 21;
    printf("\nAverage rating: %.1f\n\n", average);

    for (int star_count_i = 0; star_count_i < 5; star_count_i++) {
        printf("%i star: ", star_count_i+1);

        for (int i = 0; i < rating_frequency[star_count_i]; i++)
            printf("*");

        printf("\n");
    }

    printf("\n");

    for (int star_count_i = 0; star_count_i < 5; star_count_i++) {
        float star_count_percent = ((float) rating_frequency[star_count_i] / 21) * 100;
        printf("%i star percentage: %.1f%\n", star_count_i+1, star_count_percent);
    }

    return 0;
}
